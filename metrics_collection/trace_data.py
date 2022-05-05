import csv
import json
import ssl
import sys
import datetime
import requests
from elasticsearch import Elasticsearch, exceptions
from elasticsearch.helpers import scan
from ssl import create_default_context

from metrics_collection.trace_classes import Span, Trace, SpanReference
from metrics_collection.trace_statistics import calculate_content

JAEGER_URL = "http://10.106.121.22:16686"
services = ['ts-travel-service', 'ts-travel2-service']


def process_trace_data(trace_data):
    trace_lists = {}
    for trace in trace_data:
        # print(trace)
        # trace = trace_data[x]
        trace_id = trace["traceID"]
        trace_start_time = sys.maxsize
        trace_end_time = 0
        trace["spans"] = [span for span in trace["spans"] if span["startTime"]]
        spans = trace["spans"]
        process = trace["processes"]  # for jaeger
        for span in spans:
            start_time = span["startTime"]
            duration = span["duration"]

            if start_time < trace_start_time:
                trace_start_time = start_time

            if start_time + duration > trace_end_time:
                trace_end_time = start_time + duration

        trace_duration = round(((trace_end_time - trace_start_time) / 1000.0) * 100, 2) / 100  # converting to ms

        for span in spans:
            span["service_name"] = process[span["processID"]]["serviceName"]  # for jaeger
            # span["service_name"] = span["process"]["serviceName"] # for elasticsearch
            span["relativeStartTime"] = span["startTime"] - trace_start_time
            span["hasChildren"] = True
        # print(spans)
        trace_statistics = {}
        for span in spans:
            if span["service_name"] in trace_statistics.keys():
                trace_statistics[span["service_name"]] = calculate_content(span, spans,
                                                                           trace_statistics[span["service_name"]])
            else:
                trace_statistics[span["service_name"]] = {}
                trace_statistics[span["service_name"]]["count"] = 0
                trace_statistics[span["service_name"]]["total"] = 0
                trace_statistics[span["service_name"]]["min"] = span["duration"]
                trace_statistics[span["service_name"]]["max"] = 0
                trace_statistics[span["service_name"]]["selfMin"] = span["duration"]
                trace_statistics[span["service_name"]]["selfMax"] = 0
                trace_statistics[span["service_name"]]["selfTotal"] = 0
                trace_statistics[span["service_name"]] = calculate_content(span, spans,
                                                                           trace_statistics[span["service_name"]])
        for stats in trace_statistics:
            trace_statistics[stats]["min"] = round((trace_statistics[stats]["min"] / 1000) * 100) / 100
            trace_statistics[stats]["max"] = round((trace_statistics[stats]["max"] / 1000) * 100) / 100
            trace_statistics[stats]["total"] = round((trace_statistics[stats]["total"] / 1000) * 100) / 100
            if trace_statistics[stats]["count"]:
                trace_statistics[stats]["avg"] = trace_statistics[stats]["total"] / trace_statistics[stats]["count"]
                trace_statistics[stats]["selfAvg"] = trace_statistics[stats]["selfTotal"] / trace_statistics[stats][
                    "count"]
            trace_statistics[stats]["selfMin"] = round((trace_statistics[stats]["selfMin"] / 1000) * 100) / 100
            trace_statistics[stats]["selfMax"] = round((trace_statistics[stats]["selfMax"] / 1000) * 100) / 100
            trace_statistics[stats]["selfTotal"] = round((trace_statistics[stats]["selfTotal"] / 1000) * 100) / 100
            trace_statistics[stats]["STinDuration"] = (trace_statistics[stats]["selfTotal"] / trace_duration) * 100
        #print(json.dumps(trace_statistics))
        trace_formatted_data = {"trace_id": trace_id,
                                "duration": trace_duration,
                                "start_time": trace_start_time,
                                "end_time": trace_end_time,
                                # "spans": trace["spans"],
                                "stats": trace_statistics}
        trace_lists[trace_id] = trace_formatted_data
    return trace_lists


def jaeger_tracing(container_name, limit):
    time_delta = limit  # in minutes
    end_timestamp = datetime.datetime.now().timestamp()
    start_timestamp = datetime.datetime.now() - datetime.timedelta(minutes=time_delta)
    start_timestamp = start_timestamp.timestamp()
    # print(start_timestamp, end_timestamp)
    start_date = datetime.datetime.fromtimestamp(start_timestamp).strftime('%s') + '000000'
    end_date = datetime.datetime.fromtimestamp(end_timestamp).strftime('%s') + '000000'

    # service_name = 'ts-travel-service'
    uri = JAEGER_URL + "/api/traces?end=" + end_date + "&limit=&lookback=custom&maxDuration&minDuration&service=" + container_name + "&start=" + start_date
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    # print(uri)
    traces = requests.get(url=uri, headers=headers)
    trace_data = traces.json()
    # print(json.dumps(trace_data))
    trace_stats = process_trace_data(trace_data["data"])
    return trace_stats
    # print(json.dumps(trace_stats))


def all_traces_es(lte, gte):
    es = Elasticsearch('https://elastic:91nK0WN6fXkRz9286QCPZ22G@192.168.2.11:32699', ca_certs=False,
                       verify_certs=False, ssl_show_warn=False)
    query = {
        "query": {
            "range": {
                "startTimeMillis": {
                    "gte": "now-" + gte,
                    "lte": "now-" + lte
                }
            }
        }
    }

    # traces = es.search(index="jaeger-span-2021-04-06", body=query)
    traces = scan(es, query=query, index="jaeger-span-*")
    # print("Got %d Hits:" % traces['hits']['total']['value'])
    # print(traces)
    trace_data = []
    # for hit in traces['hits']['hits']:
    for item in traces:
        data = item["_source"]
        trace_data.append(data)

    all_traces = {}
    for spans in trace_data:
        if spans["traceID"] in all_traces:
            all_traces[spans["traceID"]]["spans"].append(spans)
        else:
            all_traces[spans["traceID"]] = {}
            all_traces[spans["traceID"]]["traceID"] = spans["traceID"]
            all_traces[spans["traceID"]]["spans"] = [spans]

    return all_traces


def aggregate_stats(containers, limit):
    all_stats = {}
    for svc in containers:
        trace_data = jaeger_tracing(svc, limit)
        for trace in trace_data:
            if trace not in all_stats:
                all_stats[trace] = trace_data[trace]
    # print(json.dumps(all_stats))
    trace_per_service = {}
    total_duration_list = []
    if not all_stats:
        return None
    for s in all_stats:
        # print(all_stats[s])
        total_duration_list.append(all_stats[s]["duration"])
        stats = all_stats[s]["stats"]
        for container in stats:
            # print(container)
            if container in trace_per_service.keys():
                trace_per_service[container]["count"].append(stats[container]["count"])
                trace_per_service[container]["total"].append(stats[container]["total"])
                trace_per_service[container]["min"].append(stats[container]["min"])
                trace_per_service[container]["max"].append(stats[container]["max"])
                trace_per_service[container]["selfMin"].append(stats[container]["selfMin"])
                trace_per_service[container]["selfMax"].append(stats[container]["selfMax"])
                trace_per_service[container]["selfTotal"].append(stats[container]["selfTotal"])
                trace_per_service[container]["avg"].append(stats[container]["avg"])
                trace_per_service[container]["selfAvg"].append(stats[container]["selfAvg"])
                trace_per_service[container]["percent"].append(stats[container]["STinDuration"])
            else:
                trace_per_service[container] = {}
                trace_per_service[container]["count"] = []
                trace_per_service[container]["total"] = []
                trace_per_service[container]["min"] = []
                trace_per_service[container]["max"] = []
                trace_per_service[container]["selfMin"] = []
                trace_per_service[container]["selfMax"] = []
                trace_per_service[container]["selfTotal"] = []
                trace_per_service[container]["avg"] = []
                trace_per_service[container]["selfAvg"] = []
                trace_per_service[container]["percent"] = []
    # print(json.dumps(trace_per_service))
    average_duration = sum(total_duration_list) / len(total_duration_list)
    for container in trace_per_service:
        if not trace_per_service[container]["count"]:
            continue
        if not trace_per_service[container]["min"]:
            continue
        # print(trace_per_service[container])
        trace_per_service[container]["count"] = sum(trace_per_service[container]["count"])
        trace_per_service[container]["total"] = sum(trace_per_service[container]["total"])
        trace_per_service[container]["min"] = min(trace_per_service[container]["min"])
        trace_per_service[container]["max"] = max(trace_per_service[container]["max"])
        trace_per_service[container]["selfMin"] = min(trace_per_service[container]["selfMin"])
        trace_per_service[container]["selfMax"] = max(trace_per_service[container]["selfMax"])
        trace_per_service[container]["selfTotal"] = sum(trace_per_service[container]["selfTotal"])
        trace_per_service[container]["avg"] = trace_per_service[container]["total"] / trace_per_service[container][
            "count"]
        trace_per_service[container]["selfAvg"] = trace_per_service[container]["selfTotal"] / trace_per_service[container]["count"]
        trace_per_service[container]["percent"] = sum(trace_per_service[container]["percent"]) / len(trace_per_service[container]["percent"])

    return trace_per_service


# aggregate_stats(services, 100)
# jaeger_tracing("ts-travel2-service", 150)
# all_traces = all_traces_es("10s", "5m")
# print(json.dumps(all_traces))
# traces_stats = process_trace_data(all_traces)
# print(json.dumps(traces_stats))
# for trace in all_traces:
#     print(json.dumps(all_traces[trace]))
# with open("train_ticket_load_test/load_data/es_data_p25_t2_all.csv", "w", newline='') as f:
#     csv_writer = csv.writer(f)
#     csv_writer.writerow(["arrival_time","service","response_time","spanID","operation_name"])
#     for line in trace_data:
#         csv_writer.writerow(line)
# train_ticket()
