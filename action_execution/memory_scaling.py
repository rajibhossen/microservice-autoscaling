import sys


def memory(pod_id, value):
    if int(value) <= 0:
        raise ValueError('Invalid Value!')

    # current_script = os.path.realpath(__file__)
    # os.system('echo %s | sudo -S python3 %s' % (SUDO_PWD, current_script))

    path = '/sys/fs/cgroup/memory' + pod_id + '/memory.limit_in_bytes'
    f = open(path, 'r')
    original = int(f.read())
    print("current Memory: " + str(original))
    new_memory = original + int(value)
    with open(path, 'r+') as f:
        data = f.read()
        f.seek(0)
        f.write(str(new_memory))
        f.truncate()
    print("New Memory: " + str(new_memory))


pod_id = sys.argv[1]
value = sys.argv[2]
memory(pod_id, value)
