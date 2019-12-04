# Theoretical plots for wastage rate models

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import math

NETSIZE = 200
# (sec)
PROPDELAY = NETSIZE/2 # TODO: what's a valid value for prop delay? - is it a function of network size?!?!
PROPDELAY = (2/3)*NETSIZE
PROPDELAY = 25
# (sec) 5 sec to 10 minutes, step by 10 seconds
INTERVALS = np.arange(5, 200, 1)  
#INTERVALS = np.array([5, 10, 15, 20, 25, 30])

# following functions return expected throughput (blocks/sec) as function of params
def harmonic_sum(k):
    k = int(k)
    total = 0
    for i in range(1, k):
        total += 1/i
    return total

def theoretical_throughput(blockinterval):
    return 1/blockinterval

def growth_rate_simple(netsize, blockinterval, propdelay):
    blocks_per_sec = 1 / blockinterval
    return blocks_per_sec # TODO: should we subtract the wastage rate??

def wastage_rate_simple(netsize, blockinterval, propdelay):
    return (netsize * propdelay) / blockinterval


# TODO: what is the correct value for lambda given a target block interval, and what is this a function of?
def growth_rate_markov(netsize, blockinterval, propdelay): # blocks/sec
    lambd = (1/blockinterval)/(netsize)
    return (netsize * lambd) - (lambd**2) * propdelay * netsize * harmonic_sum(netsize)

def wastage_rate_markov(netsize, blockinterval, propdelay):
    lambd = (1/blockinterval)/(netsize)
    return (lambd**2) * propdelay * netsize * harmonic_sum(netsize)


# we can then generate array of throughput values as function of block interval, for fixed netsize/prop delay
if __name__ == '__main__':
    # calculate result arrays:
    throughput_simple = growth_rate_simple(NETSIZE, INTERVALS, PROPDELAY)
    wastage_simple = wastage_rate_simple(NETSIZE, INTERVALS, PROPDELAY)
    throughput_markov = growth_rate_markov(NETSIZE, INTERVALS, PROPDELAY)
    wastage_markov = wastage_rate_markov(NETSIZE, INTERVALS, PROPDELAY)
    theoretical = theoretical_throughput(INTERVALS)

    fig, ax = plt.subplots()
    fig.suptitle("Throughput (Markov)")
    plt.plot(INTERVALS, throughput_markov) # , color=color)
    plt.plot(INTERVALS, theoretical, linestyle='dashed')
    ax.set(xlabel="Block Interval (sec)", ylabel="Throughput (blocks/sec)")

    fig, ax = plt.subplots()
    fig.suptitle("Wastage (Markov)")
    plt.plot(INTERVALS, wastage_markov) # , color=color)
    ax.set(xlabel="Block Interval (sec)", ylabel="Wastage Rate (blocks/sec)")
    '''
    fig, ax = plt.subplots()
    fig.suptitle("Throughput (Simple)")
    plt.plot(INTERVALS, throughput_simple) # , color=color)
    ax.set(xlabel="Block Interval (sec)", ylabel="Throughput (blocks/sec)")

    fig, ax = plt.subplots()
    fig.suptitle("Wastage (Simple)")
    plt.plot(INTERVALS, wastage_simple) # , color=color)
    ax.set(xlabel="Block Interval (sec)", ylabel="Wastage Rate (blocks/sec)")
    #fig = ax.get_figure()
    #fig.savefig("/Users/amiecorso/Desktop/SBR.pdf")
    '''
    plt.show()
    ''' color stuff
    number_of_colors = max(len(netsizes), len(intervals))
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]
    '''
