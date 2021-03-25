import sys
from action_execution.tasks import limit_cpu, limit_memory, test_task
from prometheus_data import get_metrics_data
from trace_data import jaeger_tracing


def apply_actions():
    pod_id = "/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod18784738_89c2_4589_b827_359b24966eb7.slice"
    # pod_id
    cpu_value = 1
    memory_value = 1048576
    a = 2
    b = 3
    node = "ridlserver06"

    if node == "ridlserver06":
        result = limit_memory.apply_async((pod_id, memory_value), queue='wrk06')
        print(result.get())
    elif node == "ridlserver07":
        result = limit_cpu.apply_async((a, b), queue='wrk07')
        print(result.get())
    elif node == "ridlserver08":
        result = limit_cpu.apply_async((a, b), queue='wrk08')
        print(result.get())
    elif node == "ridlserver09":
        result = limit_cpu.apply_async((a, b), queue="work09")
        print(result.get())
    elif node == "ridlserver10":
        result = limit_memory.apply_async((a, b), queue="wrk10")
        print(result.get())
    else:
        print("Invalid Node")


if __name__ == '__main__':
    system_data = get_metrics_data()
    trace_data = jaeger_tracing()
