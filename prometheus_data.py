import json
import time

from prometheus_api_client import PrometheusConnect
import requests

BASE_URL = "http://192.168.2.11:30004"
BASE_QUERY = BASE_URL + "/api/v1/query?query="
METRIC_DATA = {}
MEM_CPU_METRICS = ["container_memory_working_set_bytes",
                   "container_cpu_user_seconds_total"]
NETWORK_METRICS = ["container_network_receive_bytes_total",
                   "container_network_transmit_bytes_total"]
DISK_METRICS = ["container_fs_reads_bytes_total",
                "container_fs_writes_bytes_total"]
TIME_SCALE = "[1m]"


def get_network_data():
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


def get_disk_data():
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


if __name__ == '__main__':
    start = time.time()
    container_name = "ts-ui-dashboard"
    data = get_metrics_data(container_name)
    end = time.time()
    print("Total time in (s): ", end - start)
    print(json.dumps(data))
