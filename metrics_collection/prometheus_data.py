import json
import time
from numpy import median, percentile
# from prometheus_api_client import PrometheusConnect
import requests

BASE_URL = "http://192.168.2.62:30004"
BASE_QUERY = BASE_URL + "/api/v1/query?query="
METRIC_DATA = {}
MEM_CPU_METRICS = ["container_memory_working_set_bytes",
                   "container_cpu_user_seconds_total"]
NETWORK_METRICS = ["container_network_receive_bytes_total",
                   "container_network_transmit_bytes_total"]
DISK_METRICS = ["container_fs_reads_bytes_total",
                "container_fs_writes_bytes_total"]
TIME_SCALE = "[1m]"


def get_json_response(metric_name, container_name, duration=None):
    metric_url = metric_name + "{container=\"" + container_name + "\"}"
    if duration:
        query_url = BASE_URL + "/api/v1/query?query=" + metric_url + duration
    else:
        query_url = BASE_URL + "/api/v1/query?query=" + metric_url
    results = requests.get(url=query_url)
    query_data = results.json()
    # print(json.dumps(query_data))
    return query_data


def get_network_data(container_name):
    network_data = {}
    for metric in NETWORK_METRICS:
        metric_url = metric + "{name=~\".*" + container_name + ".*\"}"
        query_url = BASE_QUERY + metric_url + TIME_SCALE
        results = requests.get(url=query_url)
        query_data = results.json()
        nx_type = ""
        if "receive" in metric:
            nx_type = "receive"
        elif "transmit" in metric:
            nx_type = "transmit"

        for data in query_data["data"]["result"]:
            idpath = data["metric"]["id"]
            idpath = idpath.split("/")
            pod_id = idpath[3]
            docker_id = idpath[4]

            interface = data["metric"]["interface"]

            if interface == "tunl0":
                continue

            if not pod_id in network_data.keys():
                network_data[pod_id] = {}
            if not nx_type in network_data[pod_id].keys():
                network_data[pod_id][nx_type] = {}

            network_data[pod_id][nx_type][interface] = data["values"]
            network_data[pod_id]["net_docker_id"] = docker_id
            network_data[pod_id]["instance"] = data["metric"]["instance"]
    return network_data


def get_disk_data(container_name):
    disk_data = {}
    for metric in DISK_METRICS:
        metric_url = metric + "{container=\"" + container_name + "\"}"
        query_url = BASE_QUERY + metric_url + TIME_SCALE
        results = requests.get(url=query_url)
        query_data = results.json()
        ops_type = ""
        if "reads" in metric:
            ops_type = "read"
            # network_data[nx_type] = {}
        elif "writes" in metric:
            ops_type = "write"
        # network_data[nx_type] = {}
        for data in query_data["data"]["result"]:

            idpath = data["metric"]["id"]
            idpath = idpath.split("/")
            pod_id = idpath[3]
            docker_id = idpath[4]

            device = data["metric"]["device"]

            if not pod_id in disk_data.keys():
                disk_data[pod_id] = {}
            if not ops_type in disk_data[pod_id].keys():
                disk_data[pod_id][ops_type] = {}

            disk_data[pod_id][ops_type][device] = data["values"]
            disk_data[pod_id]["fs_docker_id"] = docker_id
            disk_data[pod_id]["instance"] = data["metric"]["instance"]
    return disk_data


def get_metrics_data(container_name):
    METRIC_DATA[container_name] = {}
    for metric in MEM_CPU_METRICS:
        metric_url = metric + "{container=\"" + container_name + "\"}"
        query_url = BASE_URL + "/api/v1/query?query=" + metric_url + TIME_SCALE
        results = requests.get(url=query_url)
        query_data = results.json()
        for data in query_data["data"]["result"]:
            idpath = data["metric"]["id"]

            idpath = idpath.split("/")
            pod_id = idpath[3]
            docker_id = idpath[4]

            if not pod_id in METRIC_DATA[container_name].keys():
                METRIC_DATA[container_name][pod_id] = {}

            if "cpu" in data["metric"]["__name__"]:
                METRIC_DATA[container_name][pod_id]["cpu"] = data["values"]

            if "memory" in data["metric"]["__name__"]:
                METRIC_DATA[container_name][pod_id]["memory"] = data["values"]

            METRIC_DATA[container_name][pod_id]["instance"] = data["metric"]["instance"]
            METRIC_DATA[container_name][pod_id]["mem_cpu_docker_id"] = docker_id
    network_data = get_network_data()
    for ids in network_data:
        if ids in METRIC_DATA[container_name].keys():
            METRIC_DATA[container_name][ids]["network"] = network_data[ids]

    disk_data = get_disk_data()
    for ids in disk_data:
        if ids in METRIC_DATA[container_name].keys():
            METRIC_DATA[container_name][ids]["disk"] = disk_data[ids]
    return METRIC_DATA


def prom_api():
    prom = PrometheusConnect(url=BASE_URL, disable_ssl=True)
    container_name = "ts-config-service"
    deploy_name = "ts-config-service"

    cpu_usage = prom.custom_query(query="irate(container_cpu_user_seconds_total{container=" + container_name + "}[5m])")
    # memory_usage = prom.custom_query(query="container_memory_working_set_bytes{container=\"php-apache\"}")
    # network_rx = prom.custom_query(query="irate(container_network_receive_bytes_total{pod=\"php-apache-d4cf67d68-cfgj4\"}[5m])")
    # network_rx = prom.custom_query(
    #   query="irate(container_network_receive_bytes_total{name=~\".*php-apache.*\"}[5m])")
    # network_tx = prom.custom_query(query="irate(container_network_transmit_bytes_total{name=~\".*php-apache.*\"}[5m])")

    # disk_writes = prom.custom_query(query="irate(container_fs_writes_bytes_total{container=\"php-apache\"}[5m])")
    # disk_reads = prom.custom_query(query="irate(container_fs_reads_bytes_total{container=\"php-apache\"}[5m])")
    # network_tx = prom.custom_query(query=)
    # print(float(memory_usage[0]["value"][1])/(1024.0*1024.0))
    for metric in cpu_usage:
        print(metric['metric']['id'], metric['metric']['instance'])
    # print(cpu_usage)
    # print(cpu_usage[0]["value"])
    # for container in network_tx:
    # if "php-apache" in container["metric"]["name"]:
    #    print(container["metric"]["name"], container["value"])


def get_cpu_utilization(container_name, time):
    cpu_util = get_json_response("container_cpu_usage_seconds_total", container_name, duration="["+str(time)+"m]")

    # holds each replicas metrics
    cpu_usage_each = []
    container_id = []
    for data in cpu_util["data"]["result"]:
        # keep id and node of each replicas
        container_id.append({"id": data["metric"]["id"], "node": data["metric"]["instance"]})
        cpu_time = []
        for i in range(len(data["values"]) - 1):
            cpu_time_diff = float(data["values"][i + 1][1]) - float(data["values"][i][1])
            time_diff = float(data["values"][i + 1][0]) - float(data["values"][i][0])
            cpu_time.append(cpu_time_diff / time_diff)
        if cpu_time:
            cpu_usage_each.append(sum(cpu_time) / len(cpu_time))

    # average usage over all replicas
    average_cpu_usage = sum(cpu_usage_each) / len(cpu_usage_each)

    cpu_quota = get_json_response("container_spec_cpu_quota", container_name)
    cpu_quota = cpu_quota["data"]["result"][0]["value"][1]
    cpu_period = get_json_response("container_spec_cpu_period", container_name)
    cpu_period = cpu_period["data"]["result"][0]["value"][1]
    cpu_core = (float(cpu_quota) / float(cpu_period))
    avg_cpu_utilization = average_cpu_usage / cpu_core
    return avg_cpu_utilization * 100, cpu_core, len(cpu_usage_each), container_id


def get_container_settings(container_name, time):
    cpu_util = get_json_response("container_cpu_usage_seconds_total", container_name, duration="[" + str(time) + "m]")
    container_id = []
    for data in cpu_util["data"]["result"]:
        # keep id and node of each replicas
        container_id.append({"id": data["metric"]["id"], "node": data["metric"]["instance"]})
    return container_id


def get_cpu_throttle(container_name, time):
    metric_url = "container_cpu_cfs_throttled_seconds_total" + "{container=\"" + container_name + "\"}"
    query_url = BASE_URL + "/api/v1/query?query=" + metric_url + "[" + str(time) + "m]"
    results = requests.get(url=query_url)
    cpu_util = results.json()
    # print(json.dumps(cpu_util))
    throttle_rate = 0
    num_of_points = 0
    for data in cpu_util["data"]["result"]:
        for i in range(len(data["values"]) - 1):
            throttle_change = float(data["values"][i + 1][1]) - float(data["values"][i][1])
            time_diff = float(data["values"][i + 1][0]) - float(data["values"][i][0])
            throttle_rate += throttle_change / time_diff
            num_of_points += 1
    avg_cpu_throttle = throttle_rate / num_of_points
    return avg_cpu_throttle
    # return avg_cpu_throttle


# def get_memory_usage(container_name):


def get_resource_utilization(container_name, time):
    utilization = {container_name: {}}
    # utilization[container_name]["cpu_util_avg"], utilization[container_name]["cpu_util_90"] = get_cpu_utilization(container_name)
    utilization[container_name]["cpu_util_avg_percent"], \
    utilization[container_name]["cpu_core"], \
    utilization[container_name]["replica"],\
    utilization[container_name]["settings"] = get_cpu_utilization(container_name, time)
    utilization[container_name]["cpu_throttle"] = get_cpu_throttle(container_name, time)
    return utilization


# if __name__ == '__main__':
#     start = time.time()
#     container_list =['ts-station-service', 'ts-ticketinfo-service', 'ts-route-service',
#                    'ts-travel-service', 'ts-travel2-service', 'ts-basic-service']
#     data = []
#     for container in container_list:
#         # data = get_metrics_data(container_name)
#         data.append(get_resource_utilization(container, int(120/60)))
#     print(json.dumps(data, indent=2))
#     end = time.time()
#     # print("Total time in (s): ", end - start)
#     # print(json.dumps(data))

