import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import argparse
import theoreticals as th

parser = argparse.ArgumentParser()
parser.add_argument('-f')
args = parser.parse_args()

if args.f:
    DATA = args.f
else:
    DATA = "./data/data.csv"
df = pd.read_csv(DATA)
df = df.sort_values(['nodes', 'interval'])

def wrapper_markov_growth(row):
    netsize = row['nodes']
    blockinterval = row['interval']
    propdelay = row['avg_prop_delay']
    return th.growth_rate_markov(netsize, blockinterval, propdelay)

def wrapper_markov_wastage(row):
    netsize = row['nodes']
    blockinterval = row['interval']
    propdelay = row['avg_prop_delay']
    return th.wastage_rate_markov(netsize, blockinterval, propdelay)

def wrapper_SBR_markov(row):
    theoretical_through = row['theoretical_throughput']
    wastage = row['new_wastage_markov']
    return wastage / theoretical_through

df['new_through_markov'] = df.apply(lambda row: wrapper_markov_growth(row), axis=1)
df['new_wastage_markov'] = df.apply(lambda row: wrapper_markov_wastage(row), axis=1)
df['new_SBR_markov'] = df.apply(lambda row: wrapper_SBR_markov(row), axis=1)

print(df)

netsizes = list(df["nodes"].unique())
intervals = list(df["interval"].unique())
#repeats = df["Run Index"].unique()
repeats = [1]
number_of_colors = max(len(netsizes), len(intervals))
number_of_colors = len(netsizes)

#colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]
allcolors = ['#0000FF', '#339999', '#009966', '#00CC33', '#66CC00', '#CCCC66', '#FFBF00', '#FF9900', '#CC3300', '#FF0000']
need = number_of_colors
have = len(allcolors)
colors = []
for i in range(need):
    index = int(i * (have / need))
    colors.append(allcolors[index])

# make good plots:
#fig, axes = plt.subplots(len(netsizes), 1) # two rows, len(netsize) columns
#fig.set_size_inches(10, 30)
# plot Stale Block Rates
for size in netsizes:
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 6)
    ax.set_ylim([0,1])
    fig.suptitle("SBR " + "(" + str(size) + " nodes)")
    #index = netsizes.index(size)
    #ax = axes[index]
    color = colors[netsizes.index(size)]
    for run in repeats:
        subset = df[df['nodes'] == size]
        subset.plot(x="interval", y="SBR", ax=ax, label="SimBlock", color=color)
        subset.plot(x="interval", y="new_SBR_markov", ax=ax, label="Markov", color=color, linestyle="dotted")
    ax.set(xlabel="Block Interval (sec)", ylabel="Stale Block Rate")
    legend = plt.legend(title="Legend")
    fig.savefig("/Users/amiecorso/Desktop/graphs/SBR" + str(size) + ".pdf")

#fig, axes = plt.subplots(len(netsizes), 1)
#fig.set_size_inches(10, 30)
# plot Throughput as a function of block interval
#fig, ax = plt.subplots()
for size in netsizes:
    fig, ax = plt.subplots()
    fig.suptitle("Throughput " + "(" + str(size) + " nodes)")
    fig.set_size_inches(6, 6)
    ax.set_ylim([-0.05,.2])
    #index = netsizes.index(size)
    #ax = axes[index]
    color = colors[netsizes.index(size)]
    for run in repeats:
        subset = df[df['nodes'] == size]
        subset.plot(x="interval", y="throughput", ax=ax, label="SimBlock", color=color)
        subset.plot(x="interval", y="new_through_markov", ax=ax, label="Markov", color=color, linestyle='dotted')
        subset.plot(x="interval", y="theoretical_throughput", ax=ax, label='theoretical', color='black', linestyle='dashed')
    ax.set(xlabel="Block Interval (sec)", ylabel="Throughput (blocks/sec)")
    legend = plt.legend(title="Legend")
    fig.savefig("/Users/amiecorso/Desktop/graphs/throughput" + str(size) + ".pdf")

# plot all network sizes together - THROUGHPUT
fig, axes = plt.subplots(1, 2)
fig.suptitle("Throughput")
fig.set_size_inches(12, 6)
ax = axes[0] # first column, simblock results
ax.set_title("SimBlock")
ax.set_ylim([0,.1])
for size in netsizes:
    color = colors[netsizes.index(size)]
    for run in repeats:
        subset = df[df['nodes'] == size]
        subset.plot(x="interval", y="throughput", ax=ax, label=str(size), color=color)
subset.plot(x="interval", y="theoretical_throughput", ax=ax, label='theoretical', color='black', linestyle='dashed')
ax.set(xlabel="Block Interval (sec)", ylabel="Throughput (blocks/sec)")
legend = ax.legend(title="Network Size")
ax = axes[1] # first column, simblock results
ax.set_title("Markov Model")
ax.set_ylim([0,.1])
for size in netsizes:
    color = colors[netsizes.index(size)]
    for run in repeats:
        subset = df[df['nodes'] == size]
        subset.plot(x="interval", y="new_through_markov", ax=ax, label=str(size), color=color, linestyle='dotted')
subset.plot(x="interval", y="theoretical_throughput", ax=ax, label='theoretical', color='black', linestyle='dashed')
ax.set(xlabel="Block Interval (sec)", ylabel="Throughput (blocks/sec)")
legend = plt.legend(title="Network Size")
fig.savefig("/Users/amiecorso/Desktop/graphs/throughput_all.pdf")

# plot all network sizes together - SBR
fig, axes = plt.subplots(1, 2)
fig.suptitle("Stale Block Rate")
fig.set_size_inches(12, 6)
ax = axes[0] # first column, simblock results
ax.set_title("SimBlock")
#ax.set_ylim([0,.1])
for size in netsizes:
    color = colors[netsizes.index(size)]
    for run in repeats:
        subset = df[df['nodes'] == size]
        subset.plot(x="interval", y="SBR", ax=ax, label=str(size), color=color)
ax.set(xlabel="Block Interval (sec)", ylabel="Stale Block Rate")
legend = ax.legend(title="Network Size")
ax = axes[1] # first column, simblock results
ax.set_title("Markov Model")
#ax.set_ylim([0,.1])
for size in netsizes:
    color = colors[netsizes.index(size)]
    for run in repeats:
        subset = df[df['nodes'] == size]
        subset.plot(x="interval", y="new_SBR_markov", ax=ax, label=str(size), color=color, linestyle="dotted")
ax.set(xlabel="Block Interval (sec)", ylabel="Stale Block Rate")
legend = plt.legend(title="Network Size")
fig.savefig("/Users/amiecorso/Desktop/graphs/SBR_all.pdf")

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

# plot avg prop delay as a function of block interval
fig, ax = plt.subplots()
fig.suptitle("Avg Prop Delay v.s. Block Interval")
for size in netsizes:
    color = colors[netsizes.index(size)]
    for run in repeats:
        subset = df[df['nodes'] == size]
        subset.plot(x="interval", y="avg_prop_delay", ax=ax, label=str(size) + "_SimBlock", color=color)
ax.set(xlabel="Block Interval", ylabel="Avg Prop Delay (sec)")
fig = ax.get_figure()
fig.savefig("/Users/amiecorso/Desktop/delays.pdf")

plt.show()
