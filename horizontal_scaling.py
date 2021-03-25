from kubernetes import client, config
import json

config.load_kube_config()

v1 = client.CoreV1Api()
appsv1api = client.AppsV1Api()
#ret = v1.list_pod_for_all_namespaces(watch=False)
#ret = v1.list_node()
ret = appsv1api.list_deployment_for_all_namespaces(pretty=True)

def hpa(namespace="default", deployment_name=""):
    deploy = appsv1api.read_namespaced_deployment_scale(deployment_name, namespace, pretty=True)
    current_replica = deploy.spec.replicas
    print(deployment_name, current_replica)
    deploy.spec.replicas = current_replica + 1
    new_replica = deploy
    new_replica_req = appsv1api.replace_namespaced_deployment_scale(deployment_name, namespace, new_replica)
    print(new_replica_req)

hpa(namespace="default", deployment_name="ts-ui-dashboard")



