import datetime
import json
import os
import random
import subprocess as sp
import sys
import time
import numpy as np
from scipy.interpolate import interp1d
import threading
from data_processing import end_to_end, process_utlization, get_current_configs

import client
from metrics_collection.prometheus_data import get_resource_utilization, get_container_settings
from utils.db_utils import HistoryDB

container_list = ['carts', 'catalogue', 'front-end', 'orders', 'payment', 'shipping', 'user']
EXPERIMENT_TIME = 120  # seconds
THROTTLE_PERCENTAGE = 0.01  # 1%

default = 10
container_limits = {"carts": default, "catalogue": default, "front-end": default, "orders": default, "payment": default,
                    "shipping": default,
                    "user": default}
container_throttle_limits = {"carts": 0, "catalogue": 0, "front-end": 0, "orders": 0, "payment": 0, "shipping": 0,
                             "user": 0}

container_util_list = {"carts": [], "catalogue": [], "front-end": [], "orders": [], "payment": [], "shipping": [],
                       "user": []}


def run_program(rate, experiment_time, experiment_no, threads):
    procs = []
    # two process, 1,2
    # params - script name, rate, runtime (s), log file name
    # print(threads)
    for i in range(1, threads):
        p = sp.Popen(
            [sys.executable, "sock_shop_api.py", rate, experiment_time,
             experiment_no + "/data_p" + rate + "_t" + str(threads) + "_" + str(i)])
        procs.append(p)

    for p in procs:
        p.wait()


def collect_metrics():
    container_data = []
    for container in container_list:
        container_data.append(get_resource_utilization(container, int(EXPERIMENT_TIME / 60)))
        # print(get_resource_utilization(container))
    return container_data


def avoid_cold_start():
    path = "load_data/improved_algo/temps"

    if not os.path.exists(path):
        os.makedirs(path)

    run_program(str(40), str(60), "temps", 3)
    sp.call(['sh', './flush_db.sh'])


def get_poisson_rate(requests):
    # poisson = 48901 * requests**(-1*1.053)
    rps = [1200, 1070, 960, 870, 787, 708, 650, 600, 560, 515, 470, 450, 425, 405, 380, 360, 300, 260, 226, 205, 182,
           170, 160, 147, 136, 125, 110, 95, 84, 76, 70, 64, 58, 54, 52, 49, 47, 46, 44, 42]
    poisson = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 120, 140, 160, 180, 200, 220, 240, 260,
               280, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
    x = np.array(rps)
    y = np.array(poisson)
    f = interp1d(x, y)
    poisson = f(np.array(requests))
    return int(poisson)


def apply_configurations(new_configs):
    if type(new_configs) == str:
        new_configs = eval(new_configs)

    for x in new_configs:
        settings = get_container_settings(x, 1)
        # cpu = float(new_configs[x]) / len(container_settings[x])
        cpu = round(float(new_configs[x]) / len(settings), 2)
        threads = []
        print(settings)
        for info in settings:
            print(x, info["node"], cpu, info["id"])
            # client.apply_actions(info["id"], info["node"], int(cpu * 100000))
            threads.append(
                threading.Thread(target=client.apply_cpu_resource, args=(info["id"], info["node"], int(cpu * 100000))))
            # client.apply_cpu_resource(info["id"], info["node"], int(cpu * 100000))
        for i in threads:
            i.start()
        for i in threads:
            i.join()


# {'carts': 1.9, 'catalogue': 1.3, 'front-end': 1.7, 'orders': 1.0, 'payment': 0.3, 'shipping': 0.3, 'user': 1.0}
DEFAULT_CONFIGS = {'carts': 1.5, 'catalogue': 1.0, 'front-end': 1.8, 'orders': 1.1, 'payment': 0.5, 'shipping': 0.7,
                   'user': 0.9}
# {'carts': 1.8, 'catalogue': 1, 'front-end': 1.5, 'orders': 0.8, 'payment': 0.3, 'shipping': 0.3, 'user': 0.5} for RPS 250
# {'carts': 1.9, 'catalogue': 1.3, 'front-end': 1.7, 'orders': 1.0, 'payment': 0.3, 'shipping': 0.3, 'user': 1.1} for RPS 550
# {'carts': 2.4, 'catalogue': 1.6, 'front-end': 2.6, 'orders': 1.4, 'payment': 0.6, 'shipping': 0.6, 'user': 1.5} for RPS 1050

# random.seed(1)
if __name__ == '__main__':
    SLO = 250

    ranges = {
        1: {"min": 100, "max": 200},
        2: {"min": 200, "max": 300},
        3: {"min": 300, "max": 400},
        4: {"min": 400, "max": 500},
        5: {"min": 500, "max": 600},
        6: {"min": 600, "max": 700},
        7: {"min": 700, "max": 800},
        8: {"min": 800, "max": 900},
        9: {"min": 900, "max": 1000},
        10: {"min": 1000, "max": 1100},
        11: {"min": 1100, "max": 1200}
    }

    alpha = 0.5
    beta = 0.3
    profile = 1
    experiment_no = 1
    number_of_containers = 7
    number_of_process = 5
    history = HistoryDB()
    HISTORY_WEIGHT = 1
    lower_bound = 1
    current_configurations = {}

    # avoid_cold_start()
    # avoid_cold_start()
    # avoid_cold_start()

    iteration = 3
    # rps_array = [700]
    outer_iteration = 1
    for y in range(outer_iteration):
        for x in range(iteration):

            # RPS = random.randint(975, 995)
            RPS = 550

            print("BEGIN EXPERIMENT: ", profile)
            range_id = 1
            # RPS = request_per_seconds.pop(0)
            # RPS = random.randint(605, 695)

            for x in ranges:
                if ranges[x]["min"] <= RPS < ranges[x]["max"]:
                    range_id = x
                    break

            rate = get_poisson_rate(RPS)
            print("Predicted RPS is: ", RPS)

            apply_configurations(DEFAULT_CONFIGS)

            current_settings = {"config_id": profile}
            config_name = str(profile) + "_"
            path = "load_data/improved_algo/" + config_name + str(experiment_no)

            if not os.path.exists(path):
                os.makedirs(path)

            # main experiments
            print("Starting the main experiments for 2 minutes with poisson: ", rate)
            run_program(str(rate), str(EXPERIMENT_TIME), config_name + str(experiment_no), number_of_process + 1)

            print("Collecting metrics....")
            metrics = collect_metrics()
            with open(path + "/p" + str(rate) + ".txt", 'w') as filehandle:
                json.dump(metrics, filehandle)

            # flashing databases
            sp.call(['sh', './flush_db.sh'])

            # BEGIN ALGORITHM PARTS
            start = time.time()
            rpss, responses = end_to_end(profile, EXPERIMENT_TIME)
            percentile_95 = sum(responses) / len(responses)
            rps = sum(rpss) / len(rpss)
            print("POISSON RATE IS: ", rate)
            print("RPS: %s, 95 Percentile Response: %s" % (rps, percentile_95))
            utilizations, throttles = process_utlization(profile)

            for x in utilizations:
                utilizations[x] = sum(utilizations[x]) / len(utilizations[x])

            for x in throttles:
                throttles[x] = sum(throttles[x]) / len(throttles[x])

            for x in utilizations:
                container_util_list[x].append(utilizations[x])
            current_configs, container_settings = get_current_configs(profile)

            config_cost = 0
            for c in current_configs:
                config_cost += current_configs[c]
            # config_cost = config_cost * 0.00001124444 * EXPERIMENT_TIME
            current_settings["experiment_id"] = profile
            current_settings["configs"] = current_configs
            current_settings["utils"] = utilizations
            current_settings["throttles"] = throttles
            current_settings["response"] = percentile_95
            current_settings["time"] = datetime.datetime.now()
            current_settings["rps"] = rps
            current_settings["delta_response"] = -1
            current_settings["slo"] = SLO
            current_settings["range_id"] = range_id
            current_settings["rps_range"] = ranges[range_id]
            current_settings["cost"] = config_cost
            current_settings["delta_si"] = -1
            current_settings["n_s"] = -1
            current_settings["threshold"] = -1
            current_settings["current_configs"] = current_configs
            current_settings["poisson"] = str(rate) + "x" + str(number_of_process)
            current_settings["container_stats"] = "None"  # container_stats

            history.insert_into_table(current_settings)

            end = time.time()
            duration = end - start
            print("Time to apply changes: ", duration)
            print("####################")
            profile += 1

        # DEFAULT_CONFIGS['carts'] -= 0.5
        # DEFAULT_CONFIGS['orders'] = 1.0
