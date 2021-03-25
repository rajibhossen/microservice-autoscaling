import csv

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
from datetime import datetime
from datetime import timedelta
import collections

plt.figure(figsize=(10, 6))


def log_processor():
    service_name = "pay"
    stats_file = "logs/data_p20.log"
    main_df = pd.read_csv(stats_file, parse_dates=["arrival_time"], index_col="arrival_time")

    df = main_df.loc[main_df["service"] == service_name]

    sample_average = df.response_time.resample(rule='10s').mean()
    sample_percentile = df.response_time.resample(rule='10s').quantile(0.99)
    sample_count = df.response_time.resample(rule='10s').count()
    average_latency = [x * 1000 for x in sample_average]
    percentile_99 = [x * 1000 for x in sample_percentile]
    rps = [x / 10.0 for x in sample_count]
    plt.scatter(rps, average_latency, label="Average")
    plt.scatter(rps, percentile_99, label="99 Percentile")
    # plt.plot(average_latency)
    # plt.plot(percentile_99)
    plt.legend()
    plt.xlabel("RPS")
    plt.ylabel("Response Time (ms)")
    plt.title(service_name)
    plt.show()


def parse_data():
    stats_file = "output/requests_stats_u300_w5_c.csv"
    services = ["login", "pay", "select_order", "get_foods", "finish_booking"]
    for service in services:
        main_df = pd.read_csv(stats_file, header=None)

        df = main_df.loc[main_df[2] == service + "_expected"]
        print(len(df))
        df = df.loc[df[4] == 60]

        # average = np.around(df[3].quantile(0.5), decimals=3)
        average = np.around(df[3].quantile(0.5), decimals=3)
        percent = np.around(df[3].quantile(0.99), decimals=3)
        print(service, average, percent)


def interarrival():
    service_name = "search_ticket"
    stats_file = "load_test_data.log"
    main_df = pd.read_csv(stats_file, header=None)
    # print(main_df.head())

    df = main_df.loc[main_df[3] == service_name]
    data = []
    # for index, row in df.iterrows():
    #     data.append((row[0], float(row[3])))
    for index, row in df.iterrows():
        data.append(row[2])
    # print(data)
    arrival_times = []
    # subtract response time from datetime to get the arrival times
    for i in range(len(data) - 1):
        response_time = datetime.strptime(data[i], "%Y-%m-%d %H:%M:%S.%f")
        # duration = timedelta(milliseconds=data[i][1])
        # arrival_times.append(response_time - duration)
        arrival_times.append(response_time)
    arrival_times = sorted(arrival_times)
    print(arrival_times)
    interarrival_times = []
    for i in range(len(arrival_times) - 1):
        duration = arrival_times[i + 1] - arrival_times[i]
        interarrival_times.append(duration.microseconds / 1000.0)
    interarrival_times.insert(0, 0)
    return interarrival_times


def draw_pmf(data):
    plt.figure(figsize=(10, 6))
    heights, bins = np.histogram(data, bins=50)
    heights = heights / sum(heights)
    plt.bar(bins[:-1], heights, width=(max(bins) - min(bins)) / len(bins), color="green", alpha=0.7)
    # plt.title("Food service PMF")
    # plt.savefig("output/foods_pmf.jpeg", bbox_inches="tight")
    plt.show()


def draw_data():
    # plt.figure(figsize=(10,6))
    df1 = pd.read_csv("output/requests_p20_t2_1_stats_history.csv", skiprows=(1, 200))
    df2 = pd.read_csv("output/requests_p20_t2_2_stats_history.csv", skiprows=range(1, 100))
    df3 = pd.read_csv("output/requests_p10_t2_1_stats_history.csv", skiprows=range(1, 100), skipfooter=700)
    # print(len(main_df))
    # main_df = pd.concat([df1, df2, df3])
    # print(main_df.head())
    # print(main_df["Name"])
    # df = main_df.loc[main_df["Name"] == "finish_booking" + "_expected"]
    df = df3.loc[df3["Name"] == "finish_booking" + "_expected"]

    # average = np.around(df[3].quantile(0.5), decimals=3)
    # percentile = plt.scatter(df["Requests/s"], df["99%"])
    # average = plt.scatter(df["Requests/s"], df["Total Average Response Time"])
    # plt.plot(df["99%"])
    plt.plot(df["User Count"])
    # plt.legend((percentile, average), ("99 Percentile", "Average"), loc="upper left")
    # plt.ylim(0, 5000)
    # plt.xlim(5, 30)
    plt.xlabel("RPS")
    # plt.ylabel("Latency (ms)")
    # plt.title("Food Service")
    # plt.savefig("food_service.jpeg", bbox_inches="tight")
    plt.show()


# parse_data()
# plot_latency()
# plot_request_arrival()
# data = interarrival()
# print(data)
# draw_pmf(data)
# draw_data()
log_processor()
