import time
#
from action_manager import SshClient

nodes = ["ridlserver06", "ridlserver07", "ridlserver08", "ridlserver09", "ridlserver10"]


def stress_test(nodes):
    for node in nodes:
        client = SshClient("ridl:ridl123@%s" % node)
        result = client.execute(
            "docker run --rm -it mohsenmottaghi/container-stress stress --verbose --cpu 8 --timeout 1m", sudo=True)
        print(result)


def driver_program():
    for x in range(70):
        stress_test(nodes)
        time.sleep(90)
# import subprocess
# process = subprocess.Popen(['echo', 'More output'],
#                      stdout=subprocess.PIPE,
#                      stderr=subprocess.PIPE)
# stdout, stderr = process.communicate()

if __name__ == '__main__':
    driver_program()
    # process = subprocess.Popen(['docker', 'apply', '-f', 'stress_deployment.yml'],
    #                            stdout=subprocess.PIPE,
    #                            stderr=subprocess.PIPE)
    # stdout, stderr = process.communicate()
    # time.sleep(6600)
    # process = subprocess.Popen(['kubectl', 'delete', '-f', 'stress_deployment.yml'],
    #                            stdout=subprocess.PIPE,
    #                            stderr=subprocess.PIPE)
    # stdout, stderr = process.communicate()