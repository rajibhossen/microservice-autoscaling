from .celery import app
from .scaling_proxy import memory, cpu


@app.task
def limit_cpu(pod_id, value):
    cpu(pod_id, value)


@app.task
def limit_memory(pod_id, value):
    memory(pod_id, value)


@app.task
def test_task(a,b):
    return a*b

