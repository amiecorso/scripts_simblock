# Theoretical plots for wastage rate models

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import os

# following functions return expected throughput (blocks/sec) as function of params
def growth_rate_simple(netsize, blockinterval, propdelay):
    blocks_per_sec = 1 / blockinterval
    return blocks_per_sec # TODO: should we subtract the wastage rate??

def wastage_rate_simple(netsize, blockinterval, propdelay):
    return (netsize * propdelay) / blockinterval

def growth_rate_markov(netsize, blockinterval, propdelay):
    return (netsize / blockinterval) * (1 - (propdelay / blockinterval) * (netsize - 1))

def wastage_rate_markov(netsize, blockinterval, propdelay):
    return (netsize * (netsize - 1)) * (propdelay / (blockinterval ** 2))


def growth_from_wastage(maxthrough, wastage):
    return maxthrough - wastage
# we can then generate array of throughput values as function of block interval, for fixed netsize/prop delay

NETSIZE = 32
# (sec)
PROPDELAY = 5 # TODO: what's a valid value for prop delay?
# (sec) 5 sec to 10 minutes, step by 10 seconds
INTERVALS = np.arange(5, 600, 10)  

# calculate result arrays:
throughput_simple = growth_rate_simple(NETSIZE, INTERVALS, PROPDELAY)
wastage_simple = wastage_rate_simple(NETSIZE, INTERVALS, PROPDELAY)
#throughput_markov = growth_rate_markov(NETSIZE, INTERVALS, PROPDELAY)
wastage_markov = wastage_rate_markov(NETSIZE, INTERVALS, PROPDELAY)
throughput_markov = growth_from_wastage(throughput_simple, wastage_markov)


# PLOTS
fig, ax = plt.subplots()
fig.suptitle("Throughput (Simple)")
plt.plot(INTERVALS, throughput_simple) # , color=color)
ax.set(xlabel="Block Interval (sec)", ylabel="Throughput (blocks/sec)")

fig, ax = plt.subplots()
fig.suptitle("Wastage (Simple)")
plt.plot(INTERVALS, wastage_simple) # , color=color)
ax.set(xlabel="Block Interval (sec)", ylabel="Wastage Rate (blocks/sec)")

fig, ax = plt.subplots()
fig.suptitle("Throughput (Markov)")
plt.plot(INTERVALS, throughput_markov) # , color=color)
ax.set(xlabel="Block Interval (sec)", ylabel="Throughput (blocks/sec)")

fig, ax = plt.subplots()
fig.suptitle("Wastage (Markov)")
plt.plot(INTERVALS, wastage_markov) # , color=color)
ax.set(xlabel="Block Interval (sec)", ylabel="Wastage Rate (blocks/sec)")

#fig = ax.get_figure()
#fig.savefig("/Users/amiecorso/Desktop/SBR.pdf")

plt.show()
''' color stuff
number_of_colors = max(len(netsizes), len(intervals))
colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]
'''
