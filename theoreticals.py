# Theoretical plots for wastage rate models

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import math

NETSIZES = [2096]
PROPDELAY = 30
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
    return blocks_per_sec - wastage_rate_simple(netsize, blockinterval, propdelay)

def wastage_rate_simple(netsize, blockinterval, propdelay):
    lambd = (1 / blockinterval) / (netsize)
    return lambd * propdelay * netsize # = propdelay / interval


# TODO: what is the correct value for lambda given a target block interval, and what is this a function of?
def growth_rate_markov(netsize, blockinterval, propdelay): # blocks/sec
    lambd = (1/blockinterval)/(netsize)
    return (netsize * lambd) - wastage_rate_markov(netsize, blockinterval, propdelay) 
    return (netsize * lambd) - (lambd**2) * propdelay * netsize * harmonic_sum(netsize)

def wastage_rate_markov(netsize, blockinterval, propdelay):
    lambd = (1/blockinterval)/(netsize)
    return (lambd**2) * propdelay * netsize * harmonic_sum(netsize) + delay_factor(netsize, blockinterval, propdelay)

def delay_factor(netsize, blockinterval, propdelay):
    return 0
    return  propdelay / (blockinterval ** 2.5)

# we can then generate array of throughput values as function of block interval, for fixed netsize/prop delay
if __name__ == '__main__':

    allcolors = ['#0000FF', '#339999', '#009966', '#00CC33', '#66CC00', '#CCCC66', '#FFFF00', '#FF9900', '#CC3300', '#FF0000']
    need = len(NETSIZES)
    have = len(allcolors)
    colors = []
    for i in range(need):
        index = int(i * (have / need))
        colors.append(allcolors[index])

    for NETSIZE in NETSIZES:
        color = colors[NETSIZES.index(NETSIZE)]
        # calculate result arrays:
        throughput_simple = growth_rate_simple(NETSIZE, INTERVALS, PROPDELAY)
        wastage_simple = wastage_rate_simple(NETSIZE, INTERVALS, PROPDELAY)
        throughput_markov = growth_rate_markov(NETSIZE, INTERVALS, PROPDELAY)
        wastage_markov = wastage_rate_markov(NETSIZE, INTERVALS, PROPDELAY)
        theoretical = theoretical_throughput(INTERVALS)

        fig, ax = plt.subplots()
        fig.suptitle("Throughput (Markov)" + "_" + str(NETSIZE)) 
        plt.plot(INTERVALS, throughput_markov, color=color)
        plt.plot(INTERVALS, theoretical, linestyle='dashed')
        ax.set(xlabel="Block Interval (sec)", ylabel="Throughput (blocks/sec)")

        fig, ax = plt.subplots()
        fig.suptitle("Wastage (Markov)" + "_" + str(NETSIZE))
        plt.plot(INTERVALS, wastage_markov, color=color)
        ax.set(xlabel="Block Interval (sec)", ylabel="Wastage Rate (blocks/sec)")

        fig, ax = plt.subplots()
        fig.suptitle("Throughput (Simple)" + "_" + str(NETSIZE))
        plt.plot(INTERVALS, throughput_simple, color=color)
        ax.set(xlabel="Block Interval (sec)", ylabel="Throughput (blocks/sec)")

        fig, ax = plt.subplots()
        fig.suptitle("Wastage (Simple)" + "_" + str(NETSIZE))
        plt.plot(INTERVALS, wastage_simple, color=color)
        ax.set(xlabel="Block Interval (sec)", ylabel="Wastage Rate (blocks/sec)")
        #fig = ax.get_figure()
        #fig.savefig("/Users/amiecorso/Desktop/SBR.pdf")
    plt.show()
