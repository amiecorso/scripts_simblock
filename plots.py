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
number_of_colors = len(netsizes)

#colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]
allcolors = ['#0000FF', '#339999', '#009966', '#00CC33', '#66CC00', '#CCCC66', '#FFFF00', '#FF9900', '#CC3300', '#FF0000']
need = number_of_colors
have = len(allcolors)
step = int(have/need)
colors = []
for i in range(need):
    index = int(i * (have / need))
    colors.append(allcolors[index])


# plot Stale Block Rate
fig, ax = plt.subplots()
fig.suptitle("Stale Block Rate")
for size in netsizes:
    color = colors[netsizes.index(size)]
    for run in repeats:
        subset = df[df['nodes'] == size]
        subset.plot(x="interval", y="SBR", ax=ax, label=str(size) + "_SimBlock", color=color)
        subset.plot(x="interval", y="SBR_markov", ax=ax, label=str(size) + "_Markov", color=color, linestyle="dotted")
ax.set(xlabel="Block Interval (sec)", ylabel="Stale Block Rate")
legend = plt.legend(title="Network Size")
fig = ax.get_figure()
fig.savefig("/Users/amiecorso/Desktop/SBR.pdf")
'''
# plot throughput as a function of network size
fig, ax = plt.subplots()
fig.suptitle("Throughput v.s. Network Size")
for interval in intervals:
    color = colors[intervals.index(interval)]
    for run in repeats:
        subset = df[df['interval'] == interval]
        subset.plot(x="nodes", y="throughput", ax=ax, label=str(interval), color=color)
ax.set(xlabel="Network Size", ylabel="Throughput (blocks/sec)")
fig = ax.get_figure()
fig.savefig("/Users/amiecorso/Desktop/through_vs_netsize.pdf")
'''
# plot Throughput as a function of block interval
fig, ax = plt.subplots()
fig.suptitle("Throughput v.s. Block Interval")
for size in netsizes:
    color = colors[netsizes.index(size)]
    for run in repeats:
        subset = df[df['nodes'] == size]
        subset.plot(x="interval", y="throughput", ax=ax, label=str(size) + "_SimBlock", color=color)
        subset.plot(x="interval", y="throughput_markov", ax=ax, label=str(size) + "_Markov", color=color, linestyle='dotted')
subset.plot(x="interval", y="theoretical_throughput", ax=ax, label='theoretical', color='black', linestyle='dashed')
ax.set(xlabel="Block Interval (sec)", ylabel="Throughput (blocks/sec)")
legend = plt.legend(title="Network Size")
fig = ax.get_figure()
fig.savefig("/Users/amiecorso/Desktop/through_vs_interval.pdf")
'''
# plot avg pairwise delay as a function of network size
fig, ax = plt.subplots()
fig.suptitle("Avg (pairwise) Prop Delay v.s. Network Size")
for interval in intervals:
    color = colors[intervals.index(interval)]
    for run in repeats:
        subset = df[df['interval'] == interval]
        subset.plot(x="nodes", y="avg_delay", ax=ax, label=str(interval), color=color)
ax.set(xlabel="Network Size", ylabel="Avg (pairwise) Delay (sec)")
fig = ax.get_figure()
fig.savefig("/Users/amiecorso/Desktop/delay_vs._netsize.pdf")
'''

plt.show()
