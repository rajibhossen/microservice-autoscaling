import glob
import json
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.figure(figsize=(10, 6))

base_path = "load_data/algorithm_navigation/"


def load_data_files(profile, flag):
    """
    load csv files as panda dataframes
    :return: list
    """
    logpath = base_path + str(profile)
    onlyfiles = [f for f in listdir(logpath) if isfile(join(logpath, f))]
    # print(onlyfiles)
    dataframes = []
    for f in onlyfiles:
        if f.endswith(".txt"):
            continue
        temp = pd.read_csv(logpath + "/" + f, parse_dates=["arrival_time"],
                           index_col="arrival_time")
        dataframes.append(temp)
    # print(dataframes)
    return dataframes


def end_to_end(profile):
    rpss = []
    avgs = []
    percentiles = []
    experiment_no = 1

    p = str(profile) + "_" + str(experiment_no)
    x = []
    responses = []

    data_files = load_data_files(profile=p, flag=False)
    for temp in data_files:
        df = temp
        df1 = df.groupby("user")["response_time"].agg(["count", "sum"])
        x.append(df1["count"].sum())
        for a in df1["sum"].values:
            responses.append(a)
    # print(x)
    rpss.append(sum(x) / 120.0)
    avgs.append((sum(responses) / len(responses)) * 1000)
    percentile = np.percentile(np.array(responses), 95)
    percentiles.append(percentile * 1000)

    xs, ys, zs = rpss, avgs, percentiles
    return xs, zs


def process_utlization(profile):
    experiment_no = 1
    path = base_path + str(profile) + "_" + str(experiment_no)
    txt_file = glob.glob(path + '/*.txt')
    utils = {}
    throttles = {}
    js_file = open(txt_file[0])
    data = json.load(js_file)
    for row in data:
        for key in row:
            if key in utils:
                utils[key].append(row[key]["cpu_util_avg_percent"])
                throttles[key].append(row[key]["cpu_throttle"])
            else:
                utils[key] = [row[key]["cpu_util_avg_percent"]]
                throttles[key] = [row[key]["cpu_throttle"]]

    return utils, throttles


def get_current_configs(profile):
    experiment_no = 1
    path = base_path + str(profile) + "_" + str(experiment_no)
    txt_file = glob.glob(path + '/*.txt')
    configs = {}
    container_ids = {}
    js_file = open(txt_file[0])
    data = json.load(js_file)
    for row in data:
        for key in row:
            configs[key] = row[key]['cpu_core'] * row[key]['replica']
            container_ids[key] = row[key]["settings"]
    return configs, container_ids


# print(end_to_end(1))
# print(process_utlization(1))
# print(get_current_configs(1))
# for y in range(91, 95):
#     util_list = []
#     throttle_list = []
#     utils, throttles = process_utlization(y)
#     for x in utils:
#         util_list.append(utils[x][0])
#     for x in throttles:
#         throttle_list.append(throttles[x][0])
#     print(y)
#     print(util_list)
#     print(throttle_list)
#     print("###")
# print(get_current_configs(175))
