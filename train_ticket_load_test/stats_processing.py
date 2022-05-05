import csv
import itertools
import os

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
from datetime import datetime
from datetime import timedelta
import collections
from statistics import median

plt.figure(figsize=(10, 6))


def load_data_files(profile, flag):
    """
    load csv files as panda dataframes
    :return: list
    """

    # path = "load_data/rps_350_slo_2k/"
    config = "interpolated_corrected/"

    iter1 = "/data_p25_t2_1.log"
    iter2 = "/data_p25_t2_2.log"

    path1 = "load_data/combine_rps_slo/" + profile
    path2 = "load_data/" + config + profile

    df_1 = pd.read_csv(path2 + iter1, parse_dates=["arrival_time"],
                       index_col="arrival_time")
    df_2 = pd.read_csv(path2 + iter2, parse_dates=["arrival_time"],
                       index_col="arrival_time")

    df1 = pd.concat([df_1, df_2])
    return [df_1, df_2]
    # return [df1]
    # if flag:
    #     es_60 = pd.read_csv("load_data/" + profile + "/es_data_p60_t2_all.csv", parse_dates=["arrival_time"],
    #                         index_col="arrival_time")
    #     es_55 = pd.read_csv("load_data/" + profile + "/es_data_p55_t2_all.csv", parse_dates=["arrival_time"],
    #                         index_col="arrival_time")
    #     es_50 = pd.read_csv("load_data/" + profile + "/es_data_p50_t2_all.csv", parse_dates=["arrival_time"],
    #                         index_col="arrival_time")
    #     es_45 = pd.read_csv("load_data/" + profile + "/es_data_p45_t2_all.csv", parse_dates=["arrival_time"],
    #                         index_col="arrival_time")
    #     es_40 = pd.read_csv("load_data/" + profile + "/es_data_p40_t2_all.csv", parse_dates=["arrival_time"],
    #                         index_col="arrival_time")
    #     es_35 = pd.read_csv("load_data/" + profile + "/es_data_p35_t2_all.csv", parse_dates=["arrival_time"],
    #                         index_col="arrival_time")
    #     es_30 = pd.read_csv("load_data/" + profile + "/es_data_p30_t2_all.csv", parse_dates=["arrival_time"],
    #                         index_col="arrival_time")
    #     es_25 = pd.read_csv("load_data/" + profile + "/es_data_p25_t2_all.csv", parse_dates=["arrival_time"],
    #                         index_col="arrival_time")
    #     es_65 = pd.read_csv("load_data/" + profile + "/es_data_p65_t2_all.csv", parse_dates=["arrival_time"],
    #                         index_col="arrival_time")
    #     return [es_65, es_60, es_55, es_50, es_45, es_40, es_35, es_30, es_25]
    #     # return [es_30]
    # else:
    #     df_1 = pd.read_csv("load_data/" + profile + "/data_p60_t2_1.log", parse_dates=["arrival_time"],
    #                        index_col="arrival_time", skiprows=range(1, 400))
    #     df_2 = pd.read_csv("load_data/" + profile + "/data_p60_t2_2.log", parse_dates=["arrival_time"],
    #                        index_col="arrival_time", skiprows=range(1, 400))
    #     df_3 = pd.read_csv("load_data/" + profile + "/data_p55_t2_1.log", parse_dates=["arrival_time"],
    #                        index_col="arrival_time", skiprows=range(1, 400))
    #     df_4 = pd.read_csv("load_data/" + profile + "/data_p55_t2_2.log", parse_dates=["arrival_time"],
    #                        index_col="arrival_time", skiprows=range(1, 400))
    #     df_5 = pd.read_csv("load_data/" + profile + "/data_p50_t2_1.log", parse_dates=["arrival_time"],
    #                        index_col="arrival_time", skiprows=range(1, 400))
    #     df_6 = pd.read_csv("load_data/" + profile + "/data_p50_t2_2.log", parse_dates=["arrival_time"],
    #                        index_col="arrival_time", skiprows=range(1, 400))
    #     df_7 = pd.read_csv("load_data/" + profile + "/data_p45_t2_1.log", parse_dates=["arrival_time"],
    #                        index_col="arrival_time", skiprows=range(1, 400))
    #     df_8 = pd.read_csv("load_data/" + profile + "/data_p45_t2_2.log", parse_dates=["arrival_time"],
    #                        index_col="arrival_time", skiprows=range(1, 400))
    #     df_9 = pd.read_csv("load_data/" + profile + "/data_p40_t2_1.log", parse_dates=["arrival_time"],
    #                        index_col="arrival_time", skiprows=range(1, 400))
    #     df_10 = pd.read_csv("load_data/" + profile + "/data_p40_t2_2.log", parse_dates=["arrival_time"],
    #                         index_col="arrival_time", skiprows=range(1, 400))
    #     df_11 = pd.read_csv("load_data/" + profile + "/data_p35_t2_1.log", parse_dates=["arrival_time"],
    #                         index_col="arrival_time", skiprows=range(1, 400))
    #     df_12 = pd.read_csv("load_data/" + profile + "/data_p35_t2_2.log", parse_dates=["arrival_time"],
    #                         index_col="arrival_time", skiprows=range(1, 400))
    #     df_13 = pd.read_csv("load_data/" + profile + "/data_p30_t2_1.log", parse_dates=["arrival_time"],
    #                         index_col="arrival_time", skiprows=range(1, 400))
    #     df_14 = pd.read_csv("load_data/" + profile + "/data_p30_t2_2.log", parse_dates=["arrival_time"],
    #                         index_col="arrival_time", skiprows=range(1, 400))
    #     df_15 = pd.read_csv("load_data/" + profile + "/data_p25_t2_1.log", parse_dates=["arrival_time"],
    #                         index_col="arrival_time", skiprows=range(1, 400))
    #     df_16 = pd.read_csv("load_data/" + profile + "/data_p25_t2_2.log", parse_dates=["arrival_time"],
    #                         index_col="arrival_time", skiprows=range(1, 400))
    #     df_17 = pd.read_csv("load_data/" + profile + "/data_p65_t2_1.log", parse_dates=["arrival_time"],
    #                         index_col="arrival_time", skiprows=range(1, 400))
    #     df_18 = pd.read_csv("load_data/" + profile + "/data_p65_t2_2.log", parse_dates=["arrival_time"],
    #                         index_col="arrival_time", skiprows=range(1, 400))
    #     # main_df.sort_index(inplace=True)
    #     df1 = pd.concat([df_1, df_2])
    #     df2 = pd.concat([df_3, df_4])
    #     df3 = pd.concat([df_5, df_6])
    #     df4 = pd.concat([df_7, df_8])
    #     df5 = pd.concat([df_9, df_10])
    #     df6 = pd.concat([df_11, df_12])
    #     df7 = pd.concat([df_13, df_14])
    #     df8 = pd.concat([df_15, df_16])
    #     df9 = pd.concat([df_17, df_18])
    #     # df1, df2, df3, df4, df5, df6,
    #     # return [df4,df5,df6]
    #     return [df1, df2, df3, df4, df5, df6, df7, df8, df9]


def end_to_end():
    service_name = "Overall"
    # "profile_600_75", "profile_600_125", "profile_600_150", "profile_600_200"
    for profile in ["profile_s1000_r350_25", "profile_s1100_r350_25"]:
        rpss = []
        avgs = []
        percentiles = []
        plt.figure(figsize=(10, 6))
        for p in [profile + '_1', profile + '_2', profile + '_3', profile + '_4', profile + '_5']:

            x = []
            responses = []
            # if flag true, return elasticsearch data, otherwise return laod generator data
            data_files = load_data_files(profile=p, flag=False)
            for temp in data_files:
                # df = temp.loc[temp["service"] == service_name]
                df = temp

                df1 = df.groupby("user")["response_time"].agg(["count", "sum"])
                # x = df1["count"].sum() / 180.0  # 180s experiemnt
                # y1 = df1["sum"].mean()
                # y2 = df1["sum"].quantile(0.95)
                x.append(df1["count"].sum())
                for a in df1["sum"].values:
                    responses.append(a)
            #print(responses)
            rpss.append(sum(x) / 180.0)
            avgs.append((sum(responses) / len(responses)) * 1000)
            percentile = np.percentile(np.array(responses), 95)
            percentiles.append(percentile * 1000)


        #xs, ys = zip(*sorted(zip(rpss, avgs)))
        #_, zs = zip(*sorted(zip(rpss, percentiles)))
        xs, ys, zs = rpss, avgs, percentiles

        print(profile)
        print(xs)
        print(zs)

        plt.scatter(xs, ys, label="Average Latency", marker="^", zorder=3)
        plt.scatter(xs, zs, label="95 Percentile", marker="x", zorder=3)

        plt.legend()
        plt.xlabel("RPS")
        plt.ylabel("Response Time (ms)")
        plt.title(service_name + " - " + profile)
        plt.grid(linestyle='dotted', zorder=0)
        plt.ylim(0, 3000)
        # plt.xlim(175, 375)
        # plt.savefig("figures/" + service_name + "_"+profile+"_180s.jpeg")
        plt.show()
        #break


def log_processor():
    service_name = "finish_booking"

    # profile = "profile1"
    for profile in ["profile3", "profile15", "profile16", "profile17", "profile12"]:
        rpss = []
        avgs = []
        percentiles = []
        plt.figure(figsize=(10, 6))
        for p in [profile + '_1', profile + '_2', profile + '_3', profile + '_4', profile + '_5']:
            rule = '1s'
            # if flag true, return elasticsearch data, otherwise return laod generator data
            data_files = load_data_files(profile=p, flag=False)
            for temp in data_files:
                # df = temp.loc[temp["service"] == service_name]
                df = temp

                sample_count = df.response_time.resample(rule=rule).count()
                sample_average = df.response_time.resample(rule=rule).mean()
                sample_percentile = df.response_time.resample(rule=rule).quantile(0.95)
                x = sum(sample_count) / (len(sample_count) * 1)
                y1 = sum(sample_average) / len(sample_average)
                y2 = sum(sample_percentile) / len(sample_percentile)
                avgs.append(y1 * 1000)
                rpss.append(int(x))
                percentiles.append(y2 * 1000)

        xs, ys = zip(*sorted(zip(rpss, avgs)))
        _, zs = zip(*sorted(zip(rpss, percentiles)))
        print(profile)
        print(xs)
        print(zs)

        plt.scatter(xs, ys, label="Average Latency", marker="^", zorder=3)
        plt.scatter(xs, zs, label="95 Percentile", marker="x", zorder=3)

        plt.legend()
        plt.xlabel("RPS")
        plt.ylabel("Response Time (ms)")
        plt.title(service_name + " - " + profile)
        plt.grid(linestyle='dotted', zorder=0)
        # plt.ylim(0, 700)
        # plt.xlim(175, 375)
        # plt.savefig("figures/" + service_name + "_"+profile+"_180s.jpeg")
        plt.show()
        break


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
# data = interarrival()
# print(data)
# draw_pmf(data)
# draw_data()

# log_processor()
end_to_end()
# compare_estimator()
