import csv
import json
import subprocess as sp
import sys
import time
import os

from metrics_collection.trace_data import all_traces_es
from metrics_collection.prometheus_data import get_resource_utilization

container_list = ['ts-assurance-service', 'ts-auth-service', 'ts-basic-service', 'ts-config-service',
                  'ts-consign-price-service', 'ts-consign-service', 'ts-contacts-service', 'ts-food-map-service',
                  'ts-food-service', 'ts-order-other-service', 'ts-order-service', 'ts-preserve-other-service',
                  'ts-preserve-service', 'ts-price-service', 'ts-route-plan-service',
                  'ts-route-service', 'ts-seat-service', 'ts-security-service', 'ts-station-service',
                  'ts-ticketinfo-service', 'ts-train-service', 'ts-travel-plan-service', 'ts-travel-service',
                  'ts-travel2-service', 'ts-ui-dashboard', 'ts-user-service', 'ts-news-service',
                  'ts-notification-service', 'ts-payment-service', 'ts-rebook-service', 'ts-ticket-office-service',
                  'ts-voucher-service']


def run_program(rate, experiment_no):
    procs = []
    # two process, 1,2
    # params - script name, rate, runtime (s), log file name
    for i in range(1, 3):
        p = sp.Popen(
            [sys.executable, "custom_load_test.py", rate, "180", experiment_no + "/data_p" + rate + "_t2_" + str(i)])
        procs.append(p)

    for p in procs:
        p.wait()


def collect_metrics():
    container_data = []
    for container in container_list:
        container_data.append(get_resource_utilization(container, 2))
        # print(get_resource_utilization(container))
    return container_data


# "profile_900_75", "profile_900_125", "profile_900_150",
# "profile_900_200", "profile_900_250", "profile_900_275", "profile_900_325", "profile_1200_75",
# "profile_1200_125", "profile_1200_150", "profile_1200_200", "profile_1200_250", "profile_1200_275",
# "profile_1200_325"


if __name__ == '__main__':
    profiles = ["profile_s1100_r175_60"]
    for profile in profiles:
        # print(profile)
        p = sp.Popen(["kubectl", "apply", "-f", "profiles/" + profile + ".yml"])
        p.wait()

        time.sleep(540)  # wait 10 minutes to apply changes in kubernetes

        start = time.time()
        # config_name = "profile21_"
        config_name = profile + "_"
        # run_program("30", "14")
        # # 60, 55, 50, 45, 40, 35, 30, 25, 20
        for e in range(1, 6):
            # remember to change directory in "custom_load_test" also
            path = "load_data/interpolated_corrected/" + config_name + str(e)
            if not os.path.exists(path):
                os.makedirs(path)

            """
            poisson rates ~= rps
            60 = 175, 55 = 200, 50 = 225, 45 = 250, 40 = 275, 35 = 300, 30 = 325, 25 = 350
            65 = 167, 75 = 150, 90 = 125, 110 = 100, 150 = 75, 200 = 55
            """
            profile_split = profile.split("_")
            rate = int(profile_split[3])
            # print(rate)

            run_program(str(rate), config_name + str(e))

            print("####################")
            metrics = collect_metrics()
            with open(path + "/p" + str(rate) + "_utilization.txt", 'w') as filehandle:
                json.dump(metrics, filehandle)

            time.sleep(15)

            # before 1s so, 20-1=19, and +1 for safety. runtime+sleep+1 = 300+20+1 = 621
            # trace_data = all_traces_es("9s", "190s")
            # # print(len(trace_data))
            #
            # with open("load_data/profile5_"+str(e)+"/es_data_p" + str(rate) + "_t2_all.csv", "w", newline='') as f:
            #     csv_writer = csv.writer(f)
            #     csv_writer.writerow(["arrival_time", "service", "response_time", "spanID", "operation_name"])
            #     for line in trace_data:
            #         csv_writer.writerow(line)

            sp.call(['sh', './flush_mongodb.sh'])
        print("Completed test at ", time.time() - start)
        # break
    # time.sleep(20)
