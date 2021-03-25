import os


SUDO_PWD = 'ridl123'


def memory(pod_id, value):
    dir_name = os.path.dirname(os.path.realpath(__file__))
    os.system('echo %s | sudo -S python3 %s/memory_scaling.py %s %s' % (SUDO_PWD, dir_name, pod_id, value))


def cpu(pod_id, value): 
    dir_name = os.path.dirname(os.path.realpath(__file__))
    os.system('echo %s | sudo -S python3 %s/cpu_scaling.py %s %s' % (SUDO_PWD, dir_name, pod_id, value))
