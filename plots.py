import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f')
args = parser.parse_args()

if args.f:
    DATA = args.f
else:
    DATA = "./data/data.csv"
df = pd.read_csv(DATA)
df = df.sort_values(['nodes', 'interval'])
print(df)

netsizes = list(df["nodes"].unique())
intervals = list(df["interval"].unique())
#repeats = df["Run Index"].unique()
repeats = [1]
number_of_colors = max(len(netsizes), len(intervals))

colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]

# plot Stale Block Rate
fig, ax = plt.subplots()
fig.suptitle("Stale Block Rate")
for size in netsizes:
    color = colors[netsizes.index(size)]
    for run in repeats:
        subset = df[df['nodes'] == size]
        subset.plot(x="interval", y="SBR", ax=ax, label=str(size), color=color)
ax.set(xlabel="Block Interval (ms)", ylabel="Stale Block Rate")
fig = ax.get_figure()
fig.savefig("/Users/amiecorso/Desktop/SBR.pdf")

# plot throughput as a function of network size
fig, ax = plt.subplots()
fig.suptitle("Throughput v.s. Network Size")
for interval in intervals:
    color = colors[intervals.index(interval)]
    for run in repeats:
        subset = df[df['interval'] == interval]
        subset.plot(x="nodes", y="throughput", ax=ax, label=str(interval), color=color)
ax.set(xlabel="Network Size", ylabel="Throughput (bytes/sec)")
fig = ax.get_figure()
fig.savefig("/Users/amiecorso/Desktop/through_vs_netsize.pdf")

# plot Throughput as a function of block interval
fig, ax = plt.subplots()
fig.suptitle("Throughput v.s. Block Interval")
for size in netsizes:
    color = colors[netsizes.index(size)]
    for run in repeats:
        subset = df[df['nodes'] == size]
        subset.plot(x="interval", y="throughput", ax=ax, label=str(size), color=color)
        subset.plot(x="interval", y="theoretical_throughput", ax=ax, label=str(size), color=color, linestyle='dashed')
ax.set(xlabel="Block Interval (ms)", ylabel="Throughput (bytes/sec)")
fig = ax.get_figure()
fig.savefig("/Users/amiecorso/Desktop/through_vs_interval.pdf")


plt.show()
