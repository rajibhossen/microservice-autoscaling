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
from utils.navigation_slo_threshold import get_stopping_threshold
from utils.db_utils import HistoryDB

container_list = ['carts', 'catalogue', 'front-end', 'orders', 'payment', 'shipping', 'user']
EXPERIMENT_TIME = 60  # seconds
THROTTLE_PERCENTAGE = 0.01  # 1%
DEFAULT_CONFIGS = {"carts": 5.0, "catalogue": 5.0, "front-end": 5.0, "orders": 5.0, "payment": 5.0, "shipping": 5.0,
                   "user": 5.0}
default = 10
container_limits = {"carts": default, "catalogue": default, "front-end": default, "orders": default, "payment": default,
                    "shipping": default,
                    "user": default}
container_throttle_limits = {"carts": 0, "catalogue": 0, "front-end": 0, "orders": 0, "payment": 0, "shipping": 0,
                             "user": 0}

container_util_list = {"carts": [], "catalogue": [], "front-end": [], "orders": [], "payment": [], "shipping": [],
                       "user": []}


#
# request_per_seconds = [655, 655, 651, 643, 630, 620, 616, 616, 618, 622, 630, 639, 648, 661, 675, 680, 682, 684, 687,691,
#                        693, 694, 694, 689, 681, 675, 674, 675, 676, 672, 664, 653, 640, 628, 619, 616, 616, 618, 622,631,
#                        644, 657, 668, 675, 680, 681, 683, 685, 686, 687, 688, 688, 683, 676, 671, 670, 670, 670, 668, 661,
#                        650, 637, 625, 617, 614, 614, 617, 622, 631, 643, 658, 669, 677, 680, 681, 681, 684, 686, 688, 689,
#                        689, 684, 675,668, 668, 671, 671, 668, 660, 649, 636, 624, 616, 615, 616, 617, 622, 631, 645, 658,
#                        669, 676, 678, 679, 680, 683, 685, 686, 687, 686, 681, 671, 665, 665, 666, 665, 662, 655, 644, 631,
#                        621, 613, 610, 611, 613, 617, 626, 640, 653, 663, 669, 671, 671, 670, 670, 671, 671]


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


def choose_containers(container_numbers, utilizations, throttles, current_configs):
    candidate_containers = {}
    for x in utilizations:
        if throttles[x] > THROTTLE_PERCENTAGE * EXPERIMENT_TIME:
            continue
        if current_configs[x] <= 0.3:
            continue
        candidate_containers[x] = utilizations[x]

    artificial_utils = {}
    for x in candidate_containers.keys():
        artificial_utils[x] = candidate_containers[x] / container_limits[x]
    print("ARTIFICIAL UTILS: ", artificial_utils)
    if len(candidate_containers) < container_numbers:
        return candidate_containers

    util_max = max(artificial_utils.values())
    util_min = min(artificial_utils.values())
    if util_max == util_min:
        for x in artificial_utils:
            scaled = artificial_utils[x] * 60 + 20
            artificial_utils[x] = scaled
    else:
        for x in artificial_utils:
            normalized = (artificial_utils[x] - util_min) / (util_max - util_min)
            scaled = normalized * 60 + 20
            artificial_utils[x] = scaled
    samples = {}
    for x in candidate_containers:
        if random.uniform(5, 95) > artificial_utils[x]:
            samples[x] = candidate_containers[x]
    diff = len(samples) - container_numbers
    keys = list(samples)
    data = {}
    if diff > 0:
        rng = np.random.default_rng()
        numbers = rng.choice(len(samples), len(samples) - diff, replace=False)
        for i in numbers:
            data[keys[i]] = samples[keys[i]]
        return data
    else:
        return samples


def calculate_delta_si(beta, delta_response, alpha, threshold):
    value = (beta / alpha) * min((delta_response / threshold), alpha)
    return value


def update_configurations(candidate_configs, current_configs, alpha, beta, threshold, delta_response,
                          random_exploration=0.0):
    new_configs = {}
    delta_si = calculate_delta_si(beta, delta_response, alpha, threshold)
    if random.uniform(0, 1) < random_exploration:
        print("Exploring Randomly: ", random_exploration)
        for x in candidate_configs:
            new_configs[x] = round((current_configs[x] * (1 + delta_si)), 1)
            if new_configs[x] > DEFAULT_CONFIGS[x]:
                new_configs[x] = DEFAULT_CONFIGS[x]

        for x in current_configs:
            if x not in new_configs:
                new_configs[x] = round(current_configs[x], 1)
                if new_configs[x] > DEFAULT_CONFIGS[x]:
                    new_configs[x] = DEFAULT_CONFIGS[x]
    else:
        print("Not exploring Randomly: ", random_exploration)
        for x in candidate_configs:
            new_configs[x] = round((current_configs[x] * (1 - delta_si)), 1)
            if new_configs[x] > DEFAULT_CONFIGS[x]:
                new_configs[x] = DEFAULT_CONFIGS[x]

        for x in current_configs:
            if x not in new_configs:
                new_configs[x] = round(current_configs[x], 1)
                if new_configs[x] > DEFAULT_CONFIGS[x]:
                    new_configs[x] = DEFAULT_CONFIGS[x]
    return new_configs, delta_si


def avoid_cold_start():
    path = "load_data/improved_algo/temps"

    if not os.path.exists(path):
        os.makedirs(path)

    run_program(str(60), str(120), "temps", 3)
    sp.call(['sh', './flush_db.sh'])


def get_poisson_rate(requets):
    # poisson = 48901 * requests**(-1*1.053)
    rps = [1200, 1070, 960, 870, 787, 708, 650, 600, 560, 515, 470, 450, 425, 405, 380, 360, 300, 260, 226, 205, 182,
           170, 160, 147, 136, 125, 110, 95, 84, 76, 70, 64, 58, 54, 52, 49, 47, 46, 44, 42]
    poisson = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 120, 140, 160, 180, 200, 220, 240, 260,
               280, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
    x = np.array(rps)
    y = np.array(poisson)
    f = interp1d(x, y)
    poisson = f(np.array(requets))
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


request_per_seconds_1 = [657, 657, 657, 656, 655, 654, 652, 651, 650, 644, 637, 631, 618, 605, 593, 573, 553, 533, 505,
                         480, 457, 429, 405, 384, 360, 339, 323, 305, 290, 280, 271, 265, 261, 258, 257, 258, 259, 262,
                         266, 271, 275, 279, 286, 293, 299, 308, 317, 326, 340, 354, 367, 388, 406, 423, 444, 462, 479,
                         490]
#
request_per_seconds_2 = [514, 526, 548, 566, 580, 608, 635, 660, 690, 719, 747, 779, 806, 829, 853, 870, 881, 891,899, 904,
                         909, 913, 916, 919, 923, 925, 929, 933, 937, 944, 950, 955, 963, 970, 976, 984, 991, 997, 1005,
                         1011, 1016, 1021, 1026, 1029, 1033, 1036, 1038, 1041, 1042, 1044, 1045, 1046, 1047, 1044, 1041,
                         1038, 1030, 1021, 1012, 997, 983, 968, 947, 929, 912]

request_per_seconds_3 = [895, 881, 869, 859, 851, 846, 842, 841, 842, 845, 848, 850, 854,
                         857, 859, 861, 863, 865, 863, 861, 859, 852, 845, 838, 826, 813, 800, 781, 763, 746, 723, 702,
                         682, 655, 631, 610, 582, 557, 536, 506, 480, 458, 431, 407]

request_per_seconds_4 = [388, 364, 344, 327, 309, 295, 284, 275, 269, 265, 261, 260, 260, 261, 263, 266, 270, 274, 277,
                         282, 287, 292, 300, 308, 316, 329, 342, 354, 374, 393, 411, 436, 460, 482, 512, 540, 564, 595,
                         623, 646, 675, 699, 719, 744, 765, 782, 802, 819, 832, 847, 859, 869, 879, 887, 893]

request_per_seconds_range_9 = [901, 905, 908, 912, 916, 919, 922, 925, 929, 932, 936, 939, 942, 945, 947, 951, 953, 955, 958, 961,
                         963, 966, 969, 971, 973, 975, 977, 979, 981, 983, 985, 986, 988]

request_per_seconds_range_6 = [657, 657, 657, 656, 655, 654, 652, 651, 650, 644, 637, 631, 618, 605, 608, 635, 660, 690, 682,
                               655, 631, 610, 623, 646, 675, 699]
request_per_seconds_range_2 = [290, 280, 271, 265, 261, 258, 257, 258, 259, 262, 266, 271, 275, 279, 286, 293, 299, 275, 269,
                               265, 261, 260, 260, 261, 263, 266, 270, 274, 277, 282, 287, 292]

request_per_seconds_range_3 = [384, 360, 339, 323, 305, 308, 317, 326, 340, 354, 367, 388, 300, 308, 316, 329, 342, 354, 374, 393]

# 480, 457, 429, 405, 406, 423, 444, 462, 479, 490, 411, 436, 460, 482,
request_per_seconds_range_4_5 = [480, 457, 429, 405, 406, 423, 444, 462, 479, 490, 411, 436, 460, 482,
                                 593, 573, 553, 533, 505, 514, 526, 548, 566, 580, 512, 540, 564, 595]

if __name__ == '__main__':
    # time.sleep(180)
    SLO = 250

    ranges = {
        1: {"min": 100, "max": 200},
        2: {"min": 201, "max": 300},
        3: {"min": 301, "max": 400},
        4: {"min": 401, "max": 500},
        5: {"min": 501, "max": 600},
        6: {"min": 601, "max": 700},
        7: {"min": 701, "max": 800},
        8: {"min": 801, "max": 900},
        9: {"min": 901, "max": 1000},
        10: {"min": 1001, "max": 1100},
        # 11: {"min": 1100, "max": 1200}
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
    # avoid_cold_start()
    # avoid_cold_start()

    data_size = 5
    #rps_array = [405, 415, 425, 435, 445, 455, 465, 475, 485, 495]
    # rps_array = [640, 645, 410, 410, 410, 410, 410, 740, 735]
    rps_array = []
    while data_size:
        data_size -= 1
        print("BEGIN EXPERIMENT: ", profile)
        range_id = 4
        # RPS = request_per_seconds.pop(0)

        if rps_array:
            # RPS = rps_array.pop(random.randrange(len(rps_array)))
            RPS = rps_array.pop()
        else:
            RPS = 410

        # RPS = random.randint(265, 280)
        # RPS = request_per_seconds_range_4_5.pop(0)
        # print("Predicted RPS: ", RPS)
        for x in ranges:
            if ranges[x]["min"] <= RPS <= ranges[x]["max"]:
                range_id = x
                break

        rate = get_poisson_rate(RPS)
        print("Predicted RPS is: ", RPS)

        previous_data = history.get_last_configuration(SLO, range_id)
        # print(previous_data)
        if previous_data:
            print("Got configs from DB...")
            # check if this there's new configuration
            if previous_data[0][12]:
                print("ID: %s, Experiment ID: %s, Configs: %s" % (previous_data[0][0], previous_data[0][1], previous_data[0][12]))
                apply_configurations(previous_data[0][12])
            else:
                # get configuration from history..
                data = history.get_previous_history(SLO, range_id, previous_data[0][8])
                if data:
                    print("Experiment ID: %s, Configs: %s" % (data[0][1], data[0][15]))
                    apply_configurations(data[0][15])
                else:
                    print("No configuration that matched criterias, applying default...")
                    apply_configurations(DEFAULT_CONFIGS)
        else:
            print("Applying default configs...")
            apply_configurations(DEFAULT_CONFIGS)

        current_settings = {"config_id": profile}
        config_name = str(profile) + "_"
        path = "load_data/improved_algo/" + config_name + str(experiment_no)

        if not os.path.exists(path):
            os.makedirs(path)

        # main experiments
        print("Starting the main experiments for 1 minutes with poisson: ", rate)
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

        # percentile_95 -= 20

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

        q_value = get_stopping_threshold(SLO, range_id, ranges[range_id], history, lower_bound)
        print("Q value is ", q_value)
        if q_value == -1:
            profile += 1
            print(current_settings)
            history.insert_into_table(current_settings)
            print("No changes in configs. Conducting same experiments...")
            print("######################")
            continue

        threshold = (((lower_bound * SLO - q_value) / (ranges[range_id]["max"] - ranges[range_id]["min"])) * (
                rps - ranges[range_id]["min"])) + q_value

        print("Threshold for RPS: %d is %d" % (rps, threshold))

        delta_response = max(0, threshold - percentile_95)
        current_settings["delta_response"] = delta_response
        current_settings["threshold"] = threshold

        if percentile_95 > threshold:
            """
            select previous configuration that didn't violate SLO
            """
            print("Response time exceeded threshold. Will go back to history")
            print(current_settings)
            current_settings["configs"] = ""
            history.insert_into_table(current_settings)

            # time.sleep(60)
        else:
            for x in utilizations:  # update limit of containers.
                max_value = max(container_util_list[x])
                if max_value > container_limits[x]:
                    container_limits[x] = max_value

            for x in throttles:  # update throttle of containers
                if throttles[x] >= container_throttle_limits[x]:
                    container_throttle_limits[x] = throttles[x]
            # select_container_numbers = int((number_of_containers / alpha) * (delta_response / SLO))
            select_container_numbers = int((number_of_containers / alpha) * (delta_response / threshold))

            if select_container_numbers > number_of_containers:
                select_container_numbers = number_of_containers

            candidate_containers = choose_containers(select_container_numbers, utilizations, throttles, current_configs)

            # random_explore = 1 - ((number_of_containers - select_container_numbers) / number_of_containers)
            # random_explore = 0.2
            random_explore = (delta_response / (alpha * SLO)) * 0.04 + 0.01
            new_configs, delta_si = update_configurations(candidate_containers, current_configs, alpha, beta, threshold,
                                                          delta_response, random_exploration=random_explore)

            current_settings["configs"] = new_configs
            current_settings["delta_si"] = delta_si
            current_settings["n_s"] = select_container_numbers
            print("N_s: ", current_settings["n_s"], "Threshold: ", current_settings["threshold"])
            print("New configs: ", current_settings["configs"])
            history.insert_into_table(current_settings)

            # time.sleep(60)

        end = time.time()
        duration = end - start
        print("Current Utilizations Limit: ", container_util_list)
        print("Current Throttle Limit: ", container_throttle_limits)
        print("Time to apply changes: ", duration)
        print("####################")
        profile += 1
