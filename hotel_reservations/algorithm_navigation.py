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

container_list = ['hotel-reserv-frontend', 'hotel-reserv-geo', 'hotel-reserv-profile', 'hotel-reserv-rate',
                  'hotel-reserv-recommendation',
                  'hotel-reserv-reservation', 'hotel-reserv-search', "hotel-reserv-user"]
EXPERIMENT_TIME = 120  # seconds
THROTTLE_PERCENTAGE = 0.00085  # 1%

DEFAULT_CONFIGS = {'hotel-reserv-frontend': 4, 'hotel-reserv-geo': 3, 'hotel-reserv-profile': 3, 'hotel-reserv-rate': 3,
                   'hotel-reserv-recommendation': 3, 'hotel-reserv-reservation': 3, 'hotel-reserv-search': 3,
                   "hotel-reserv-user": 3}

default = 10
container_limits = {'hotel-reserv-frontend': default, 'hotel-reserv-geo': default, 'hotel-reserv-profile': default,
                    'hotel-reserv-rate': default,
                    'hotel-reserv-recommendation': default, 'hotel-reserv-reservation': default,
                    'hotel-reserv-search': default, "hotel-reserv-user": default}

container_throttle_limits = {'hotel-reserv-frontend': 0, 'hotel-reserv-geo': 0, 'hotel-reserv-profile': 0,
                             'hotel-reserv-rate': 0,
                             'hotel-reserv-recommendation': 0, 'hotel-reserv-reservation': 0, 'hotel-reserv-search': 0,
                             "hotel-reserv-user": 0}

container_util_list = {'hotel-reserv-frontend': [], 'hotel-reserv-geo': [], 'hotel-reserv-profile': [],
                       'hotel-reserv-rate': [],
                       'hotel-reserv-recommendation': [], 'hotel-reserv-reservation': [], 'hotel-reserv-search': [],
                       "hotel-reserv-user": []}
request_per_seconds = [577.8, 575, 558, 514, 453.2, 403.4, 380.8, 381.4, 392.8, 414.4, 452.6, 497.8, 543.6, 609.2,
                       673.6, 701.2, 710.8, 721.6, 738.2, 754.6, 766, 771.6, 769.8, 747.8, 706, 676.4, 672.4, 679,
                       679.6, 662, 621.2, 565.8, 503.6, 443.2, 398.6, 381.2, 383.2, 393.6, 414.8, 457.2, 519.2, 585.8,
                       641, 678.2, 699, 709.2, 717.6, 724.6, 731.4, 737, 742, 739.6, 718.6, 682.6, 657.6, 651.4, 652.4,
                       652.2, 640.2, 604.6, 549, 485.8, 427.2, 385.6, 370.6, 374.2, 386.8, 410.6, 455.2, 520.2, 590.4,
                       647.8, 685.2, 703.4, 707, 710, 720, 733.2, 743.2, 748.8, 746.2, 720.2, 676.4, 643.2, 641, 655.2,
                       656.2, 637.8, 600.4, 545.2, 481.8, 423.6, 385.8, 376.2, 380.6, 389.8, 413.2, 458.6, 524.4, 593.8,
                       646.2, 678.8, 694, 698.4, 704.2, 715, 726, 734, 738.6, 733.4, 704.6, 659.2, 630.4, 626.8, 630.4,
                       628.4, 612.4, 574.8, 520.2, 459, 404.8, 369, 355.2, 356.2, 365.6, 388.2, 434.4, 499.4, 566,
                       615.8, 644.4, 658.4, 658.2, 653.4, 653.8, 655.6, 655.8, 653, 640.8, 611, 566, 523, 495.8, 485.6,
                       486.2, 484.8, 471.8, 445, 411, 373.8, 340.2, 317.2, 309.6, 313.6, 325.4, 349.8, 385, 426.6,
                       470.8, 510.6, 539.2, 557, 567.2, 573.2, 578.8, 587, 594.8, 591, 572.2, 546.4, 520.8, 503.4,
                       499.2, 502.6, 502, 489, 464.6, 432, 395.2, 361.2, 337.4, 330.2, 335.8, 350, 374.8, 412.6, 458.2,
                       502.8, 543, 578.2, 608.4, 636.8, 660, 673.2, 674.8, 674, 671.2, 657.2, 636.8, 628.8, 631.4,
                       631.6, 629.8, 621.8, 589.4, 533.6, 471.4, 417.6, 383, 372.2, 378.2, 390.2, 416.2, 463.6, 529.4,
                       597.8, 651, 686.8, 707.6, 723, 739, 755, 768.4, 778.4, 783.8, 771, 733.2, 689.4, 668.8, 667.4,
                       663.6, 653.4, 632.4, 589.6, 527.2, 462.2, 409.2, 377.4, 368.6, 375.6, 392.4, 423.8, 479.2, 553.4,
                       620.2, 666.4, 695.4, 714.8, 729.4, 740.4, 750, 760, 764.8, 762.6, 748.8, 714.2, 671.8, 652.2,
                       653.2, 655, 649, 625.6, 583, 522.4, 457.2, 406.4, 377.2, 369.6, 374.6, 392.2, 430.2, 488.8,
                       561.4, 626.6, 674.4, 706.2, 721.2, 728, 738.6, 749.8, 757, 759.6, 759.8, 745.8, 709.6, 663.2,
                       642, 645.6, 648.2, 640.2, 616.2, 573.4, 516.2, 454.8, 405.4, 375.4, 363, 369.8, 392.4, 432.4,
                       493.4, 568.6, 634.6, 679.4, 707.2, 718.6, 724.2, 733, 742, 749.4, 751.6, 746.8, 728, 691.2,
                       650.2, 625.8, 619.4, 614.4, 604.6, 586.2, 547.4, 489.2, 430.2, 382.4, 353.8, 349.6, 359.2, 374.8,
                       409.2, 464.8, 534.8, 594.4, 632.8, 655.6, 662.2, 659.2, 657, 657, 655.8, 652.8, 650.2, 639.6,
                       611.6, 572, 531, 503.6, 492.2, 487, 480, 465.2, 437.8, 401.8, 366.6, 337.8, 320.8, 317.8, 326.6,
                       346, 377.8, 420.2, 466.8, 508.4, 539.4, 560.2, 573.8, 583, 590.8, 595.2, 597, 595, 588, 571.8,
                       548.4, 528.8, 521.8, 523.6, 525.8, 518.2, 496, 465.4, 430.6, 394.8, 364.6, 348.8, 349.4, 357.8,
                       372.2, 400.2, 439.8, 488.2, 534, 572, 604.2, 629.6, 653.6, 675.6, 693, 705.8, 708.8, 702.8,
                       687.4, 672.8, 656.2, 625.6, 593.4, 574, 528.8, 466.8, 421.8, 390.4, 374.8, 384.8, 412.6, 451,
                       488.6, 525.4, 592.6, 675.6, 712.8, 709.2, 734.2, 747.4, 758.6, 777.2, 769, 763.6, 751.4, 709.6,
                       673.8, 675.8, 672, 666.2, 672.4, 638.6, 572.8, 500.8, 440.4, 398, 378, 377.2, 391, 405.8, 438.2,
                       501.8, 566, 628.8, 678, 679.4, 679.2, 697, 715.6, 718, 728.4, 740.2, 733, 702.6, 691, 672.6,
                       655.2, 666.6, 660.2, 655.6, 613.8, 546.2, 495, 440.6, 392.8, 369.8, 371.8, 395.6, 417.2, 443.2,
                       497, 582.6, 659, 692.6, 693, 685, 694.6, 700.4, 714.4, 730.8, 732, 750.6, 747, 694.2, 640, 626.6,
                       653.4, 666.6, 643.8, 603.6, 545.8, 480.2, 420.4, 385.4, 377.8, 378, 385.2, 409.2, 454.8, 518.4,
                       575.2, 631.4, 680.6, 698.4, 706.8, 718.8, 730.6, 732, 726, 728, 718.8, 682, 648.6, 624.4, 606.8,
                       612.4, 625, 611.4, 579.6, 530.8, 464.4, 419.8, 381.4, 351.4, 346.6, 357.2, 379.6, 421.2, 484,
                       557, 619, 637.6, 655.2, 681.6, 680.4, 666.6, 653.8, 654, 663, 649.4, 620, 589.8, 547.4, 506,
                       487.6, 482.2, 483.6, 475.4, 462, 431.6, 384.6, 354, 323.8, 302.2, 309.4, 325.8, 348.4, 384.4,
                       414, 453.2, 505.6, 534.8, 559.8, 567.2, 562.4, 563.6, 582.6, 608, 606, 574.6, 541.6, 529.4,
                       515.8, 495.4, 486.2, 487.2, 484.2, 464.8, 436.2, 403, 370.6, 340.2, 319.8, 327.2, 349.2, 379.6,
                       417.8, 462, 500.4, 548, 599.4, 623.8, 638, 652, 657.6, 657.6, 667.6, 668.8, 658.6, 632.6, 622.2,
                       624.6, 626.6, 648.4, 645.4, 606.2, 549, 491.8, 434, 388.4, 379.6, 382, 380, 399.6, 455.8, 527.6,
                       585, 632.2, 687.8, 717, 737.8, 755, 753.2, 761.4, 780.8, 791, 774.2, 749.6, 707.2, 676.4, 676.8,
                       660, 648.2, 639.6, 605.8, 551.2, 472.2, 402.2, 366.4, 359, 364.8, 376.6, 409.6, 466.4, 543.8,
                       615.6, 662.2, 691, 718.2, 732.8, 748.6, 762.8, 745.4, 754.6, 768.2, 746.8, 729.2, 705.8, 691.8,
                       677, 649.8, 644.4, 638.6, 588.8, 527, 472.6, 419, 387.6, 372.6, 364.6, 374.8, 415.4, 471.4,
                       536.6, 612.2, 671.2, 695, 714.6, 724.4, 731.8, 738.4, 748.6, 755.2, 745.4, 727.6, 709.8, 679,
                       643, 642.4, 659.8, 658.6, 644.6, 601.6, 530.8, 458.2, 407.2, 371.2, 359.6, 363.4, 376, 419,
                       475.4, 542.2, 607.2, 642.6, 678.2, 715.8, 722.4, 720.8, 724.6, 746.2, 767, 770.8, 745, 702.6,
                       670, 637.8, 608.2, 592, 578.2, 575.2, 546.6, 484.6, 416.4, 369.4, 350.2, 350.6, 354, 367.8,
                       394.6, 444.8, 524.4, 593, 628.4, 659, 669.8, 640, 627.4, 632.8, 646.2, 665.8, 658.6, 619.8,
                       599.6, 586.2, 546.4, 512.2, 491.4, 480.4, 474, 460.2, 443.8, 410.2, 369.8, 345, 321.2, 309.8,
                       317.8, 338.2, 369.2, 402.2, 447, 497.4, 534.2, 561.4, 573.2, 585.8, 598.8, 592.4, 587.4, 585,
                       584.4, 566.8, 548.4, 537.8, 516.4, 515.6, 532.8, 521, 491, 464.8, 434.2, 394.2, 365.4, 352,
                       354.2, 364, 370.8, 395, 440.6, 492.4, 526.8, 563.4, 613, 629.6, 633, 650.2, 666.4, 690.4, 725,
                       718, 688.2, 665.4, 645.8, 609.6, 572.2, 565, 541.8, 484, 419, 388.4, 384.6, 389.4, 405.8, 428.8,
                       478.2, 536.2, 595.2, 657.6, 686.8, 701.4, 699.4, 697.6, 739.8, 780.2, 793.8, 787.2, 755.8, 717.8,
                       675, 668.2, 691, 688, 665.8, 636.8, 587.8, 533.8, 464.8, 410, 386.8, 385.2, 389.6, 407.8, 446.4,
                       495.2, 547.6, 608.4, 662.6, 677.6, 685, 701, 720.2, 724.6, 728.6, 736, 727.6, 720.6, 690.2, 661,
                       664.4, 663, 668]


def run_program(rate, experiment_time, experiment_no, threads):
    procs = []
    # two process, 1,2
    # params - script name, rate, runtime (s), log file name
    # print(threads)
    for i in range(1, threads):
        p = sp.Popen(
            [sys.executable, "load_test.py", rate, experiment_time,
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
        if throttles[x] > 0.02:
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
        for x in candidate_configs:
            new_configs[x] = max(DEFAULT_CONFIGS[x], round((current_configs[x] * (1 + delta_si)), 1))

        for x in current_configs:
            if x not in new_configs:
                new_configs[x] = round(current_configs[x], 1)
    else:
        for x in candidate_configs:
            new_configs[x] = round((current_configs[x] * (1 - delta_si)), 1)

        for x in current_configs:
            if x not in new_configs:
                new_configs[x] = round(current_configs[x], 1)
    return new_configs, delta_si


def avoid_cold_start():
    path = "load_data/algorithm_navigation/temps"

    if not os.path.exists(path):
        os.makedirs(path)

    run_program(str(45), str(60), "temps", 3)
    # sp.call(['sh', './flush_db.sh'])


def get_poisson_rate(requests):
    # poisson = 32684 * requests**(-1*1.049)
    rps = [840.5083333, 708.1833333, 613.3666667, 544.9333333, 483.4333333, 432.8, 393.3, 364.0583333, 339.7416667,
           315.3416667, 295]
    poisson = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
    #
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


if __name__ == '__main__':
    SLO = 50

    ranges = {
        1: {"min": 100, "max": 200},
        2: {"min": 201, "max": 300},
        3: {"min": 301, "max": 400},
        4: {"min": 401, "max": 500},
        5: {"min": 501, "max": 600},
        6: {"min": 601, "max": 700},
        7: {"min": 701, "max": 800},
        8: {"min": 801, "max": 900}
    }

    # ranges = {
    #     1: {"min": 100, "max": 300},
    #     2: {"min": 301, "max": 500},
    #     3: {"min": 501, "max": 700}
    # }

    # ranges = {
    #     1: {"min": 100, "max": 150},
    #     2: {"min": 151, "max": 200},
    #     3: {"min": 201, "max": 250},
    #     4: {"min": 251, "max": 300},
    #     5: {"min": 301, "max": 350},
    #     6: {"min": 351, "max": 400},
    #     7: {"min": 401, "max": 450},
    #     8: {"min": 451, "max": 500},
    #     9: {"min": 501, "max": 550},
    #     10: {"min": 551, "max": 600},
    #     11: {"min": 601, "max": 650},
    #     12: {"min": 651, "max": 700},
    #     13: {"min": 701, "max": 750},
    #     14: {"min": 751, "max": 800}
    # }

    alpha = 0.6
    beta = 0.3
    profile = 1
    experiment_no = 1
    number_of_containers = len(container_list)
    number_of_process = 10
    history = HistoryDB()
    HISTORY_WEIGHT = 1
    lower_bound = 1
    current_configurations = {}

    avoid_cold_start()
    # avoid_cold_start()
    # avoid_cold_start()

    data_size = 30
    rps_array = [305, 315, 325, 335, 345, 355, 365, 375, 385, 395]
    while data_size:
        data_size -= 1
        print("BEGIN EXPERIMENT: ", profile)

        range_id = 2
        # RPS = 100
        # RPS = request_per_seconds.pop(0)
        # if rps_array:
        #     RPS = rps_array.pop(random.randrange(len(rps_array)))
        # else:
        #     RPS = random.randint(575, 595)

        RPS = random.randint(375, 395)
        # RPS = request_per_seconds.pop(0)

        # RPS = 650
        if profile > 10:
            beta = 0.2
        if profile > 20:
            beta = 0.1
        if profile > 40:
            beta = 0.05

        for x in ranges:
            if ranges[x]["min"] <= RPS < ranges[x]["max"]:
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
                print("Experiment ID: %s, Configs: %s" % (previous_data[0][1], previous_data[0][12]))
                apply_configurations(previous_data[0][12])
            else:
                # get configuration from history..
                data = history.get_previous_history(SLO, range_id, previous_data[0][8])
                # print(data)
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
        path = "load_data/algorithm_navigation/" + config_name + str(experiment_no)

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
        # sp.call(['sh', './flush_db.sh'])

        # BEGIN ALGORITHM PARTS
        start = time.time()
        rpss, responses = end_to_end(profile)
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
            # random_explore = delta_response / (alpha * SLO* (profile-10))
            new_configs, delta_si = update_configurations(candidate_containers, current_configs, alpha, beta, threshold,
                                                          delta_response, random_exploration=0)

            current_settings["configs"] = new_configs
            current_settings["delta_si"] = delta_si
            current_settings["n_s"] = select_container_numbers
            print("N_s: ", current_settings["n_s"], "Threshold: ", current_settings["threshold"])
            print("New configs: ", current_settings["configs"])
            history.insert_into_table(current_settings)

            # CODE for dynamic range

            # if select_container_numbers < 3 and select_container_numbers != -1:
            #     if range_id in ns_changed_total:
            #         ns_changed_total[range_id] += 1
            #     else:
            #         ns_changed_total[range_id] = 0
            #
            # if range_id in ns_changed_total and ns_changed_total[range_id] == 5:
            #     ns_changed_total[range_id] = 0
            #     available_range_id = 0
            #     for x in ranges:
            #         if available_range_id <= x:
            #             available_range_id = x
            #     available_range_id += 1
            #
            #     range_min = ranges[range_id]["min"]
            #     range_max = ranges[range_id]["max"]
            #
            #     if range_max - range_min < 10:
            #         continue
            #
            #     ranges[range_id]["min"] = range_min
            #     ranges[range_id]["max"] = range_min + int((range_max - range_min) / 2)
            #
            #     ranges[available_range_id] = {}
            #     ranges[available_range_id]["min"] = range_min + int((range_max - range_min) / 2) + 1
            #     ranges[available_range_id]["max"] = range_max
            #
            #     ns_changed_total[available_range_id] = 0
            #
            #     save_q_value(SLO, available_range_id, q_value, QValueDB())
            #     current_settings["range_id"] = available_range_id
            #     current_settings["rps_range"] = ranges[available_range_id]
            #     history.insert_into_table(current_settings)

        end = time.time()
        duration = end - start
        print("Time to apply changes: ", duration)
        print("####################")
        profile += 1
        # time.sleep(30)
