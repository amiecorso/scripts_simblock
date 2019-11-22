import os
import subprocess
import shutil
import argparse
from datetime import datetime


NET_PATH = "/Users/amiecorso/simblock/simulator/src/main/java/SimBlock/settings/NetworkConfiguration.java"
SIM_PATH = "/Users/amiecorso/simblock/simulator/src/main/java/SimBlock/settings/SimulationConfiguration.java"
OUT_DIR = "/Users/amiecorso/simblock/simulator/src/dist/output/"
RESULTS_DIR = "/Users/amiecorso/scripts/results/"
DATA_DIR = "/Users/amiecorso/scripts/data/"
ARCHIVE_DIR = "/Users/amiecorso/scripts/archive/"

# SETTING COMBINATIONS
NUM_NODES = [1, 2, 4, 8, 16, 32, 64, 128] #[1, 2, 4, 8, 16, 32, 64, 128, 256]
BLOCK_INTERVALS =[sec * 1000 for sec in [5, 10, 20, 30, 40, 50, 80, 100]] # milliseconds
BLOCK_SIZES = [535000] # bytes
ENDBLOCKHEIGHT = 400

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

def calc_throughput(filepath):
    ''' Return throughput as bytes/sec for given experiment '''
    with open(filepath, 'r') as f:
        lines = f.readlines()
    blocksize = int(filepath.split("_")[2])
    for line in lines[::-1]:
        if "OnChain" in line:
            splitline = line.split(":")
            height = int(splitline[1].strip())
            gen_time = int(splitline[-1].strip())
            return round((height * blocksize) / gen_time, 2)
    return 0


def process_results(results_dir):
    ''' Generate CSV summary of data from output files '''
    results = []
    for f in os.listdir(results_dir):
        if "blocklist" in f:
            SBR = calc_SBR(results_dir + f)
            throughput = calc_throughput(results_dir + f)
            splitname = f.split("_")
            nodes, interval, size = splitname[:3]
            results.append(','.join((str(nodes), str(interval), str(size), str(SBR), str(throughput))) + '\n')
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    with open(DATA_DIR + 'data.csv', 'w') as outfile:
        outfile.write(','.join(('nodes', 'interval', 'blocksize', 'SBR', 'throughput')) + '\n')
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
    if not os.path.exist(ARCHIVE_DIR):
        os.mkdir(ARCHIVE_DIR)
    for nodecount in NUM_NODES:
        for interval in BLOCK_INTERVALS:
            for size in BLOCK_SIZES:
                write_sim_config(nodecount, interval, size, ENDBLOCKHEIGHT)
                build_and_run()
                blocklist_path, output_path = collect_outputs((nodecount, interval, size))
    process_results(RESULTS_DIR)
    # move experimental results to archive dir



main()
