import json
import sys
import datetime
import requests

JAEGER_URL = "http://192.168.2.11:32688"
services = ['ts-order-service', 'ts-auth-service', 'ts-basic-service']


def jaeger_tracing():
    time_delta = 1  # in minutes
    end_timestamp = datetime.datetime.now().timestamp()
    start_timestamp = datetime.datetime.now() - datetime.timedelta(minutes=1)
    start_timestamp = start_timestamp.timestamp()
    # print(start_timestamp, end_timestamp)
    # start_date = datetime.datetime.fromtimestamp(start_timestamp).strftime('%s') + '000000'
    # end_date = datetime.datetime.fromtimestamp(end_timestamp).strftime('%s') + '000000'

    start_date = "1614028834144000"
    end_date = "1614032434144000"

    service_name = 'ts-travel-service'
    uri = JAEGER_URL + "/api/traces?end=" + end_date + "&limit=&lookback=custom&maxDuration&minDuration&service=" + service_name + "&start=" + start_date
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    print(uri)
    traces = requests.get(url=uri, headers=headers)
    trace_data = traces.json()
    # print(json.dumps(trace_data))
    trace_map = []
    for trace in trace_data["data"]:
        trace_id = trace["traceID"]
        trace_start_time = sys.maxsize
        trace_end_time = 0
        span_map = {}
        span_id_counts = {}
        for spans in trace["spans"]:
            span_id = spans["spanID"]
            start_time = spans["startTime"]
            duration = spans["duration"]
            process_id = spans["processID"]

            if start_time < trace_start_time:
                trace_start_time = start_time

            if start_time + duration > trace_end_time:
                trace_end_time = start_time + duration

            # span_id_count = span_id_counts.get(span_id)
            # if not span_id_count:
            #     span_id_counts[span_id] = int(span_id_count) + 1
            # else:
            #     span_id_counts[span_id] = 1
            # span_id = str(span_id) + "_" + str(span_id_count)
            # span_map[span_id] = spans
        total_latency = (trace_end_time - trace_start_time) / 1000.0  # converting to ms
        trace_formatted_data = {"trace_id": trace_id,
                                "duration": total_latency,
                                "start_time": trace_start_time,
                                "end_time": trace_end_time,
                                "spans": trace["spans"],
                                "processes": trace["processes"]}
        trace_map.append(trace_formatted_data)
        # print(trace_formatted_data)
        # break
    total_request = len(trace_map)
    request_per_sec = total_request / (time_delta*60.0)
    return [
        request_per_sec,
        trace_map
    ]


if __name__ == '__main__':
    data = jaeger_tracing()
    #print(json.dumps(data))
    # train_ticket()
