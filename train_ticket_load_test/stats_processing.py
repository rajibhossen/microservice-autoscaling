import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# response_times = []
# with open("output/full_stats.csv", "r", newline="")as stats_file:
#     reader = csv.reader(stats_file)
#     for row in reader:
#         if row[1] == "finish_booking_expected":
#             response_times.append(float(row[2]))
plt.figure(figsize=(10, 6))
import pandas as pd

df = pd.read_csv("output/flat_load_stats_history.csv")
# print(df.head())
service_name = "login_expected"
df = df.loc[df["Name"] == service_name]
print(len(df))

fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:green'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('Response Time (ms)', color=color)
ax1.plot(df["Timestamp"], df["50%"], color=color, linestyle="-", label="Median")
ax1.plot(df["Timestamp"], df["99%"], color=color, linestyle="-.", label="99 Percentile")
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend()
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('# of Users', color=color)  # we already handled the x-label with ax1
ax2.plot(df["Timestamp"], df["User Count"], color=color, linestyle="--", label="# of User")
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc="upper left")

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.title(service_name)
plt.show()
