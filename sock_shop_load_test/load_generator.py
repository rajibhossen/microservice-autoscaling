import csv
import json
import subprocess as sp
import sys
import time
import os

from metrics_collection.trace_data import all_traces_es
from metrics_collection.prometheus_data import get_resource_utilization

container_list = ['carts', 'catalogue', 'front-end', 'orders', 'payment', 'shipping', 'user']


def run_program(rate, experiment_time, experiment_no):
    procs = []
    # two process, 1,2
    # params - script name, rate, runtime (s), log file name
    for i in range(1, 3):
        p = sp.Popen(
            [sys.executable, "sock_shop_api.py", rate, experiment_time,
             experiment_no + "/data_p" + rate + "_t2_" + str(i)])
        procs.append(p)

    for p in procs:
        p.wait()


def collect_metrics():
    container_data = []
    for container in container_list:
        container_data.append(get_resource_utilization(container))
        # print(get_resource_utilization(container))
    return container_data


if __name__ == '__main__':
    # profiles = ["profile1"]
    for profile in range(2, 8):

        p = sp.Popen(["kubectl", "apply", "-f", "profiles/" + str(profile) + ".yaml"])
        p.wait()

        # time.sleep(240)  # wait 4 minutes to apply changes in kubernetes

        # initial run to avoid cold start
        run_program("150", "30", "discard")
        sp.call(['sh', './flush_db.sh'])

        start = time.time()
        config_name = str(profile) + "_"
        for e in range(1, 7):
            time.sleep(30)
            # remember to change directory in "sock_shop" also
            path = "load_data/rps_200_slo_100/" + config_name + str(e)
            if not os.path.exists(path):
                os.makedirs(path)
            # poisson = rps
            # 275 = 50, 150 = 100, 100 = 150, 77 = 200, 58 = 250, 48 = 300, 38 = 350, 33 = 400

            # profile_split = profile.split("_")
            # rate = int(profile_split[3])
            rate = 75

            run_program(str(rate), "180", config_name + str(e))

            print("####################")

            metrics = collect_metrics()
            with open(path + "/p" + str(rate) + "_t2_utilization.txt", 'w') as filehandle:
                json.dump(metrics, filehandle)

            sp.call(['sh', './flush_db.sh'])
        print("Completed test at ", time.time() - start)
        # break
