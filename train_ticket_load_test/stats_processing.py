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
    service_name = "finish_booking"
    # stats_file = "load_data/data_p20_t5.log"
    # main_df = pd.read_csv(stats_file, parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 10000))
    # main_df.sort_index(inplace=True)

    df_1 = pd.read_csv("load_data/data_p65_t2_1.log", parse_dates=["arrival_time"], index_col="arrival_time",
                       skiprows=range(1, 4000))
    df_2 = pd.read_csv("load_data/data_p65_t2_2.log", parse_dates=["arrival_time"], index_col="arrival_time",
                       skiprows=range(1, 4000))
    df_3 = pd.read_csv("load_data/data_p60_t2_1.log", parse_dates=["arrival_time"], index_col="arrival_time",
                       skiprows=range(1, 1000))
    df_4 = pd.read_csv("load_data/data_p60_t2_2.log", parse_dates=["arrival_time"], index_col="arrival_time",
                       skiprows=range(1, 1000))
    df_5 = pd.read_csv("load_data/data_p55_t2_1.log", parse_dates=["arrival_time"], index_col="arrival_time",
                       skiprows=range(1, 1000))
    df_6 = pd.read_csv("load_data/data_p55_t2_2.log", parse_dates=["arrival_time"], index_col="arrival_time",
                       skiprows=range(1, 1000))
    df_7 = pd.read_csv("load_data/data_p50_t2_1.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_8 = pd.read_csv("load_data/data_p50_t2_2.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_9 = pd.read_csv("load_data/data_p45_t2_1.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_10 = pd.read_csv("load_data/data_p45_t2_2.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_11 = pd.read_csv("load_data/data_p40_t2_1.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_12 = pd.read_csv("load_data/data_p40_t2_2.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_13 = pd.read_csv("load_data/data_p35_t2_1.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_14 = pd.read_csv("load_data/data_p35_t2_2.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_15 = pd.read_csv("load_data/data_p30_t2_1.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_16 = pd.read_csv("load_data/data_p30_t2_2.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_17 = pd.read_csv("load_data/data_p25_t2_1.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_18 = pd.read_csv("load_data/data_p25_t2_2.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_19 = pd.read_csv("load_data/data_p20_t2_1.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))
    df_20 = pd.read_csv("load_data/data_p20_t2_2.log", parse_dates=["arrival_time"], index_col="arrival_time", skiprows=range(1, 1000))

    # dfs = []
    # for rate in [65, 60, 55, 50, 45, 40, 35, 30, 25, 20]:
    #     for i in range(1, 3):
    #         df = pd.read_csv("load_data/data_p" + str(rate) + "_t2_" + str(i) + ".log", parse_dates=["arrival_time"],
    #                          index_col="arrival_time")
    #         dfs.append(df)

    # main_df.sort_index(inplace=True)
    df1 = pd.concat([df_1, df_2])
    df2 = pd.concat([df_3, df_4])
    df3 = pd.concat([df_5, df_6])
    df4 = pd.concat([df_7, df_8])
    df5 = pd.concat([df_9, df_10])
    df6 = pd.concat([df_11, df_12])
    df7 = pd.concat([df_13, df_14])
    df8 = pd.concat([df_15, df_16])
    df9 = pd.concat([df_17, df_18])
    df10 = pd.concat([df_19, df_20])
    rpss = []
    avgs = []
    percentiles = []
    # df2, df3, df4, df5, df6, df7, df8, df9,df10
    for temp in [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10]:

        df = temp.loc[temp["service"] == service_name]

        sample_average = df.response_time.resample(rule='30s').mean()
        sample_percentile = df.response_time.resample(rule='30s').quantile(0.99)
        sample_count = df.response_time.resample(rule='30s').count()
        average_latency = [x * 1000 for x in sample_average]
        percentile_99 = [x * 1000 for x in sample_percentile]
        rps = [x / 30.0 for x in sample_count]
        for x in average_latency:
            avgs.append(x)
        for x in rps:
            rpss.append(x)
        for x in percentile_99:
            percentiles.append(x)
    # print(rps)
    # print(average_latency)
    # print(rpss)
    # print(avgs)
    plt.scatter(rpss, avgs, label="Average Latency")
    plt.scatter(rpss, percentiles, label="99 Percentile")
    # plt.plot(average_latency)
    # plt.plot(rps)
    # plt.plot(percentile_99)
    plt.ylim(0, 3000)
    #plt.xlim(15, 50)
    plt.legend(loc="upper left")
    plt.xlabel("RPS")
    plt.ylabel("Response Time (ms)")
    plt.title(service_name)
    #plt.savefig("figures/" + service_name + "_10s.jpeg")
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
    stats_file = "load_data/data_p60_t2_2.log"
    main_df = pd.read_csv(stats_file)
    # print(main_df.head())

    df = main_df.loc[main_df["service"] == service_name]
    arrival_times = []
    for index, row in df.iterrows():
        arrival_times.append(datetime.strptime(row["arrival_time"], "%Y-%m-%d %H:%M:%S.%f"))

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
    plt.title("Search Ticket PMF")
    plt.xlabel("Inter Arrival Time (ms)")
    plt.savefig("figures/search_ticket_pmf.jpeg", bbox_inches="tight")
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
#data = interarrival()
#print(data)
#draw_pmf(data)
# draw_data()
log_processor()
