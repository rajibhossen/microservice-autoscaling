from prometheus_api_client import PrometheusConnect


def print_metrics():
    prom = PrometheusConnect(url="http://10.100.114.33:9090", disable_ssl=True)

    print(prom.all_metrics())


def print_one_metric():
    prom = PrometheusConnect(url="http://10.100.114.33:9090", disable_ssl=True)
    # print(prom.custom_query(query="container_cpu_usage_seconds_total{image!=\"\",container!=\"POD\"}"))
    print(prom.custom_query(query="rate(container_cpu_user_seconds_total{container=\"php-apache\"}[5m])"))


if __name__ == '__main__':
    # print_metrics()
    print_one_metric()
