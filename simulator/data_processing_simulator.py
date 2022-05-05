import csv
import glob
import itertools
import json
import os
import random
from os import listdir
from os.path import isfile, join
from sympy import symbols, Eq

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
from datetime import datetime
from datetime import timedelta
import collections
from statistics import median

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


def utilization_equations(container, config, range_id):
    # print(container, config, range_id)
    data = {
        'ts-assurance-service': {'1': 0.02966, '2': 0.03727, '3': 0.05459, '4': 0.06858, '5': 0.08229, '6': 0.09482},
        'ts-auth-service': {'1': 1.38924, '2': 1.64689, '3': 2.46738, '4': 2.99391, '5': 3.91903, '6': 4.48878},
        'ts-basic-service': {'1': 0.24705, '2': 0.29353, '3': 0.44935, '4': 0.54912, '5': 0.74931, '6': 0.88532},
        'ts-config-service': {'1': 0.04483, '2': 0.0528, '3': 0.0788, '4': 0.0962, '5': 0.12472, '6': 0.14173},
        'ts-consign-price-service': {'1': 0.01626, '2': 0.01586, '3': 0.02506, '4': 0.02884, '5': 0.03782, '6': 0.0407},
        'ts-consign-service': {'1': 0.03467, '2': 0.04096, '3': 0.06096, '4': 0.07152, '5': 0.08845, '6': 0.10388},
        'ts-contacts-service': {'1': 0.05998, '2': 0.0706, '3': 0.10532, '4': 0.12555, '5': 0.16174, '6': 0.18618},
        'ts-food-map-service': {'1': 0.03077, '2': 0.03959, '3': 0.05216, '4': 0.06316, '5': 0.07997, '6': 0.09219},
        'ts-food-service': {'1': 0.04555, '2': 0.05499, '3': 0.0826, '4': 0.0978, '5': 0.12667, '6': 0.14155},
        'ts-order-other-service': {'1': 0.03661, '2': 0.04351, '3': 0.06093, '4': 0.07223, '5': 0.09595, '6': 0.10772},
        'ts-order-service': {'1': 0.13671, '2': 0.15902, '3': 0.23857, '4': 0.30657, '5': 0.4055, '6': 0.46817},
        'ts-preserve-other-service': {'1': 0.00072, '2': 0.00084, '3': 0.00083, '4': 0.00086, '5': 0.00085,
                                      '6': 0.00083},
        'ts-preserve-service': {'1': 0.08116, '2': 0.09844, '3': 0.14764, '4': 0.17895, '5': 0.24298, '6': 0.27623},
        'ts-price-service': {'1': 0.05192, '2': 0.06288, '3': 0.09356, '4': 0.11291, '5': 0.14581, '6': 0.16843},
        'ts-route-plan-service': {'1': 0.00068, '2': 0.00069, '3': 0.00084, '4': 0.00083, '5': 0.00131, '6': 0.00094},
        'ts-route-service': {'1': 0.20801, '2': 0.24322, '3': 0.37017, '4': 0.44229, '5': 0.58211, '6': 0.67529},
        'ts-seat-service': {'1': 0.11219, '2': 0.13102, '3': 0.19604, '4': 0.2494, '5': 0.30006, '6': 0.34688},
        'ts-security-service': {'1': 0.04687, '2': 0.05554, '3': 0.0811, '4': 0.09857, '5': 0.12611, '6': 0.14312},
        'ts-station-service': {'1': 0.29026, '2': 0.33469, '3': 0.50947, '4': 0.62792, '5': 0.80027, '6': 0.93295},
        'ts-ticketinfo-service': {'1': 0.17957, '2': 0.21587, '3': 0.32243, '4': 0.3937, '5': 0.52222, '6': 0.57365},
        'ts-train-service': {'1': 0.10511, '2': 0.12237, '3': 0.18724, '4': 0.2229, '5': 0.30945, '6': 0.36665},
        'ts-travel-plan-service': {'1': 0.00071, '2': 0.00077, '3': 0.00082, '4': 0.0014, '5': 0.0008, '6': 0.00087},
        'ts-travel-service': {'1': 0.29268, '2': 0.32842, '3': 0.50188, '4': 0.59685, '5': 0.79295, '6': 0.89576},
        'ts-travel2-service': {'1': 0.07649, '2': 0.08862, '3': 0.13179, '4': 0.15619, '5': 0.21341, '6': 0.24855},
        'ts-user-service': {'1': 0.03972, '2': 0.04366, '3': 0.06174, '4': 0.08711, '5': 0.09539, '6': 0.10637},
        'ts-rebook-service': {'1': 0.00208, '2': 0.00206, '3': 0.0022, '4': 0.00224, '5': 0.00279, '6': 0.0031},
        'ts-ticket-office-service': {'1': 0.00025, '2': 0.00026, '3': 0.00025, '4': 0.00026, '5': 0.00025,
                                     '6': 0.00028}}
    if str(int(range_id)) not in data[container]:
        data[container][str(int(range_id))] = data[container]["4"] #(data[container]["4"] + data[container]["5"]) / 2
    value = data[container][str(int(range_id))]
    return (value / config) * 100


def process_utlization(rps, current_configs, range_id):
    utils = {}
    throttles = {}
    for key in current_configs:
        utils[key] = utilization_equations(key, current_configs[key], range_id)
        throttles[key] = random.uniform(0, 3)
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
