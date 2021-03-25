import sys

SUDO_PWD = 'ridl123'


def cpu(pod_id, value, period=100000):
    if int(value) <= 0:
        raise ValueError('Invalid Value!')

    current_script = os.path.realpath(__file__)
    # print(current_script)
    # os.system('echo %s | sudo -S python3 %s' % (SUDO_PWD, current_script))
    print('cpu - id: ' + pod_id + ' - delta: ' + str(value))

    path = '/sys/fs/cgroup/cpu' + pod_id + '/cpu.cfs_quota_us'
    f = open(path, 'r')
    original = int(f.read())
    print('original quota: ' + str(original))
    new_value = original + int(value)
    with open(path, 'r+') as f:
        data = f.read()
        f.seek(0)
        f.write(str(new_value))
        f.truncate()


pod_id = sys.argv[1]
value = sys.argv[2]
cpu(pod_id, value)
