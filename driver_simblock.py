import os
import subprocess
import shutil
import argparse
from datetime import datetime
import numpy as np
import theoreticals as th


NET_PATH = "/Users/amiecorso/simblock/simulator/src/main/java/SimBlock/settings/NetworkConfiguration.java"
SIM_PATH = "/Users/amiecorso/simblock/simulator/src/main/java/SimBlock/settings/SimulationConfiguration.java"
OUT_DIR = "/Users/amiecorso/simblock/simulator/src/dist/output/"
RESULTS_DIR = "/Users/amiecorso/scripts/results/"
DATA_DIR = "/Users/amiecorso/scripts/data/"
ARCHIVE_DIR = "/Users/amiecorso/scripts/archive/"

# SETTING COMBINATIONS
NUM_NODES = [1, 8, 32, 128, 512, 2096] #[1, 2, 4, 8, 16, 32, 64, 128, 256]
BLOCK_INTERVALS =[sec * 1000 for sec in np.arange(5, 200, 5)] # milliseconds
BLOCK_SIZES = [535000 * 50] # bytes
ENDBLOCKHEIGHT = 100
'''
NUM_NODES = [1, 4, 16, 32, 128] #[1, 2, 4, 8, 16, 32, 64, 128, 256]
BLOCK_INTERVALS =[sec * 1000 for sec in np.arange(5, 600, 10)] # milliseconds
BLOCK_SIZES = [535000] # bytes
ENDBLOCKHEIGHT = 400
'''
#tiny test
NUM_NODES = [200] #[1, 2, 4, 8, 16, 32, 64, 128, 256]
BLOCK_INTERVALS =[sec * 1000 for sec in [30]] # milliseconds
BLOCK_SIZES = [535000 * 10] # bytes
ENDBLOCKHEIGHT = 50 


def write_sim_config(nodes, interval, blocksize, endblockheight):
    ''' Update the SimulationConfiguration.java file with given parameters'''
    with open(SIM_PATH, "r") as simconfig:
        contents = simconfig.readlines()
        # line 18 : NUM_OF_NODES
        contents[18] = " ".join(contents[18].split()[:-1]) + ' ' + str(nodes) + ";\n"
        # line 23 : INTERVAL
        contents[23] = " ".join(contents[23].split()[:-1]) + ' ' + str(interval) + ";\n"
        # line 32 : BLOCKSIZE
        contents[32] = " ".join(contents[32].split()[:-1]) + ' ' + str(blocksize) + ";\n"
        contents[29] = " ".join(contents[29].split()[:-1]) + ' ' + str(endblockheight) + ";\n"
    with open(SIM_PATH, "w") as simconfig:
        simconfig.writelines(contents)


def build_and_run():
    ''' rebuild simblock with given settings '''
    os.chdir("/Users/amiecorso/simblock")
    subprocess.run(["gradle", "clean", "build"])
    subprocess.run(["gradle", ":simulator:run"])


def collect_outputs(settings):
    os.chdir(OUT_DIR)
    now = ''.join('_'.join(str(datetime.now()).split()).split(".")[:-1])
    settings_prefix = ''
    for sett in settings:
        settings_prefix += str(sett) + "_"
    blocklist_path = RESULTS_DIR + settings_prefix + "blocklist_" + now
    output_path = RESULTS_DIR + settings_prefix + "output_" + now
    shutil.move(OUT_DIR + 'blockList.txt', blocklist_path)
    shutil.move(OUT_DIR + 'output.json', output_path)
    #subprocess.run(["rm", OUT_DIR + 'output.json']) # we only want the blocklist! not this long output file
    return (blocklist_path, output_path)


def calc_SBR(filepath):
    ''' Return Stale Block Rate (SBR) for given experiment '''
    total_count = 0
    orphan_count = 0
    with open(filepath, 'r') as f:
        for line in f:
            if "Orphan" in line:
                orphan_count += 1
            total_count += 1
    return round(orphan_count / total_count, 2)

def calc_throughput_blocks(filepath):
    ''' Return throughput as bytes/sec for given experiment '''
    with open(filepath, 'r') as f:
        lines = f.readlines()
    for line in lines[::-1]: # reversed blocklist
        if "OnChain" in line: # find the first real one
            splitline = line.split(":")
            height = int(splitline[1].strip())
            gen_time = int(splitline[-1].strip()) / 1000 # ms to sec
            return height / gen_time # can't round!! because the numbers are already very small?
    return 0

def calc_throughput_bytes(filepath):
    ''' Return throughput as bytes/sec for given experiment '''
    with open(filepath, 'r') as f:
        lines = f.readlines()
    blocksize = int(filepath.split("_")[2])
    for line in lines[::-1]:
        if "OnChain" in line:
            splitline = line.split(":")
            height = int(splitline[1].strip())
            gen_time = int(splitline[-1].strip()) / 1000 # ms to sec
            return round((height * blocksize) / gen_time, 2)
    return 0


def get_avg_pairwise_delay(filename):
    with open(filename, 'r') as f:
        contents = f.read()

    total_proptime = 0
    numsamples = 0
    aslist = eval(contents)
    for item in aslist:
        if item['kind'] == 'flow-block':
            info = item['content']
            trans_stamp = info['transmission-timestamp']
            recv_stamp = info['reception-timestamp']
            proptime_ms = recv_stamp - trans_stamp
            total_proptime += proptime_ms
            numsamples += 1
    total_proptime /= 1000 # ms to sec
    return round(total_proptime / numsamples, 5)

def process_results(results_dir, outfile_name):
    ''' Generate CSV summary of data from output files '''
    results = []
    for f in os.listdir(results_dir):
        if "blocklist" in f:
            try:
                outputjson = f.replace("blocklist", "output") 
                avg_delay = get_avg_pairwise_delay(results_dir + outputjson)
            except:
                print("Couldn't find file: ", outputjson, "...")
                avg_delay = "NaN"
            SBR = calc_SBR(results_dir + f)
            throughput = calc_throughput_blocks(results_dir + f)
            splitname = f.split("_")
            nodes, interval, size = splitname[:3]
            nodes = int(nodes)
            size = int(size)
            interval = int(interval) / 1000 # ms to sec
            theoretical_through = 1 / int(interval)
            growth_rate_markov = th.growth_rate_markov(nodes, interval, avg_delay)
            waste_rate_markov = th.wastage_rate_markov(nodes, interval, avg_delay)
            SBR_markov = waste_rate_markov / theoretical_through
            results.append(','.join((str(nodes), str(interval), str(size), str(SBR), str(throughput), str(theoretical_through), str(avg_delay), str(growth_rate_markov), str(waste_rate_markov), str(SBR_markov))) + '\n')
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    with open(DATA_DIR + outfile_name, 'w') as outfile:
        outfile.write(','.join(('nodes', 'interval', 'blocksize', 'SBR', 'throughput', 'theoretical_throughput', 'avg_delay', 'throughput_markov', 'waste_rate_markov', 'SBR_markov')) + '\n')
        outfile.writelines(results)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-test', action='store_true')
    args = parser.parse_args()

    if args.test:
        subprocess.run(["rm", "-rf", RESULTS_DIR])
        subprocess.run(["rm", "-rf", DATA_DIR])

    if not os.path.exists(RESULTS_DIR):
        os.mkdir(RESULTS_DIR)
    if not os.path.exists(ARCHIVE_DIR):
        os.mkdir(ARCHIVE_DIR)
    for nodecount in NUM_NODES:
        for interval in BLOCK_INTERVALS:
            for size in BLOCK_SIZES:
                write_sim_config(nodecount, interval, size, ENDBLOCKHEIGHT)
                build_and_run()
                blocklist_path, output_path = collect_outputs((nodecount, interval, size))
    now = ''.join('_'.join(str(datetime.now()).split()).split(".")[:-1])
    datafilename = "data_" + now + ".csv"
    process_results(RESULTS_DIR, datafilename)
    # move experimental results to archive dir
    results_name = RESULTS_DIR.rstrip("/") + "_" + now
    #subprocess.run(["mv", RESULTS_DIR, results_name])
    #subprocess.run(["cp", "-r", results_name, ARCHIVE_DIR])
    #subprocess.run(["rm", "-rf", results_name])
    # actually just destroy the huge output files:
    subprocess.run(["rm", "-rf", RESULTS_DIR])


if __name__ == '__main__':
    main()
