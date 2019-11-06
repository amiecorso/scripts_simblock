import os
import subprocess
import shutil
from datetime import datetime


NET_PATH = "/Users/amiecorso/simblock/simulator/src/main/java/SimBlock/settings/NetworkConfiguration.java"
SIM_PATH = "/Users/amiecorso/simblock/simulator/src/main/java/SimBlock/settings/SimulationConfiguration.java"
OUT_DIR = "/Users/amiecorso/simblock/simulator/src/dist/output/"
RESULTS_DIR = "/Users/amiecorso/scripts/results/"

# SETTING COMBINATIONS
NUM_NODES = [1, 2, 4] #[1, 2, 4, 8, 16, 32, 64, 128, 256]
BLOCK_INTERVALS = [5, 10, 20] #[5, 10, 20, 40, 80, 120, 240, 300] # seconds
BLOCK_SIZES = [535000] # bytes

def write_sim_config(nodes, interval, blocksize):
    ''' Update the SimulationConfiguration.java file with given parameters'''
    with open(SIM_PATH, "r") as simconfig:
        contents = simconfig.readlines()
        # line 18 : NUM_OF_NODES
        contents[18] = " ".join(contents[18].split()[:-1]) + ' ' + str(nodes) + ";\n"
        # line 23 : INTERVAL
        contents[23] = " ".join(contents[23].split()[:-1]) + ' ' + str(interval) + ";\n"
        # line 32 : BLOCKSIZE
        contents[32] = " ".join(contents[32].split()[:-1]) + ' ' + str(blocksize) + ";\n"
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
    blocklist_path = settings_prefix + "blocklist_" + now
    output_path = settings_prefix + "output_" + now
    shutil.move(OUT_DIR + 'blockList.txt', RESULTS_DIR + blocklist_path)
    shutil.move(OUT_DIR + 'output.json', RESULTS_DIR + output_path)



def main():
    if not os.path.exists(RESULTS_DIR):
        os.mkdir(RESULTS_DIR)
    for nodecount in NUM_NODES:
        for interval in BLOCK_INTERVALS:
            for size in BLOCK_SIZES:
                write_sim_config(nodecount, interval, size)
                build_and_run()
                collect_outputs((nodecount, interval, size))

main()
