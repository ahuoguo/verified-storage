# initially generated by claude.ai

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from statistics import mean, stdev
from pathlib import Path
import argparse
import sys
import csv
import scipy.stats as st
import json

kvstores = ["redis", "pmemrocksdb", "viper", "capybarakv"]
nice_kvstore_names = ["pmem-Redis", "pmem-RocksDB", "Viper", "CapybaraKV"]
workloads = ["sequential_put", "sequential_get", "sequential_update", "sequential_delete", 
    "rand_put", "rand_get", "rand_update", "rand_delete"]
nice_workload_names = ["Seq\nput", "Seq\nget", "Seq\nupdate", "Seq\ndelete",
    "Rand\nput", "Rand\nget", "Rand\nupdate", "Rand\ndelete"]

list_kvstores = ["redis", "capybarakv"]
nice_list_kvstore_names = ["pmem-Redis", "CapybaraKV"]

list_workloads = ["rand_list_append", "rand_list_len", "rand_list_read", "rand_list_trim",]
nice_list_workload_names = ["Append", "Len", "Read list", "Trim"]

def process_workload_file(file_path):
    with open(file_path, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]

def process_workload_directory(workload_dir):
    print("Processing directory", workload_dir)
    values = []
    
    # Process all files in the directory
    for filename in os.listdir(workload_dir):
        file_path = os.path.join(workload_dir, filename)
        if os.path.isfile(file_path):
            try:
                file_values = process_workload_file(file_path)
                values.extend(file_values)
            except (ValueError, IOError) as e:
                print(f"Warning: Couldn't process file {file_path}: {str(e)}")
                continue
    
    if not values:
        print(f"Warning: No valid data found in directory {workload_dir}")
        return 0, 0

    mean_latency = mean(values)
    stdev_latency = stdev(values)
    conf_int = st.t.interval(0.95, df=len(values)-1, loc=mean_latency, scale=st.sem(values))
    conf_int_for_plot = [mean_latency - conf_int[0], conf_int[1] - mean_latency]

    return mean_latency, stdev_latency, conf_int_for_plot if len(values) > 1 else 0

def parse_files(result_dir):
    if not os.path.exists(result_dir):
        print(f"Error: Directory '{result_dir}' does not exist")
        sys.exit(1)
        
    results = {}
    
    # Process each KV store directory
    for kvstore in os.listdir(result_dir):
        kvstore_path = os.path.join(result_dir, kvstore)
        if not os.path.isdir(kvstore_path):
            continue
            
        results[kvstore] = {}
        
        # Process each workload in the KV store directory
        # for workload in os.listdir(kvstore_path):
        for workload in workloads:
            workload_path = os.path.join(kvstore_path, workload)
            if not os.path.isdir(workload_path):
                continue
                
            mean_val, std_val, conf_int = process_workload_directory(workload_path)
            results[kvstore][workload] = (mean_val, std_val, conf_int)
        
        for workload in list_workloads:
            workload_path = os.path.join(kvstore_path, workload)
            if not os.path.isdir(workload_path):
                continue
                
            mean_val, std_val, conf_int = process_workload_directory(workload_path)
            results[kvstore][workload] = (mean_val, std_val, conf_int)
    
    if not results:
        print(f"Error: No valid data found in directory '{result_dir}'")
        sys.exit(1)
        
    return results

def save_results_to_json(results, output_file):
    json_string = json.dumps(results)
    with open(output_file, "w") as f:
        f.write(json_string)

def read_results_from_json(input_file):
    with open(input_file, "r") as f:
        json_string = f.read()
        results = json.loads(json_string)
    return results

def plot_results(ax, results):
    # mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["cornflowerblue", "orange", "mediumpurple", "black"]) 
    
    # Set up the plot
    # ax.figure(figsize=(4.6, 1.8))
    x = np.arange(len(workloads))
    width = 0.8 / len(kvstores)
    # plt.set_axisbelow(True)
    
    # Plot bars for each KV store
    for i, kvstore in enumerate(kvstores):
        means = [results[kvstore][w][0] for w in workloads]
        err1 = [results[kvstore][w][2][0] for w in workloads]
        err2 = [results[kvstore][w][2][1] for w in workloads]
        err = [err1, err2]

        if kvstore == kvstores[0]:
            hatch = "////"
            color = "cornflowerblue"
        elif kvstore == kvstores[1]:
            hatch= ".."
            color = "orange"
        elif kvstore == kvstores[2]:
            hatch = "xx"
            color = "mediumpurple"
        else:
            hatch = ""
            color = "black"
        
        ax.bar(x + i*width - width*len(kvstores)/2 + width/2, 
                means,
                width,
                label=kvstore,
                yerr=err,
                hatch=hatch,
                error_kw=dict(ecolor="red", capsize=1), 
                zorder=4,
                color=color)
        
    ax.grid(True, zorder=3, axis="y")
    ax.set_xlabel("(a) Item operations")
    ax.set_ylabel('Latency (us)')
    ax.set_yscale("log")
    
    ax.set_xticks(x, nice_workload_names, fontsize="8")

def plot_list_results(ax, results):
    x = np.arange(len(list_workloads))
    width = 0.8 / len(list_kvstores)
    
    # Plot bars for each KV store
    for i, kvstore in enumerate(list_kvstores):
        means = [results[kvstore][w][0] for w in list_workloads]
        err1 = [results[kvstore][w][2][0] for w in list_workloads]
        err2 = [results[kvstore][w][2][1] for w in list_workloads]
        err = [err1, err2]

        if kvstore == kvstores[0]:
            hatch = "////"
            color = "cornflowerblue"
        else:
            hatch = ""
            color = "black"
        
        ax.bar(x + i*width - width*len(list_kvstores)/2 + width/2, 
                means,
                width,
                label=kvstore,
                yerr=err,
                hatch=hatch,
                error_kw=dict(ecolor="red", capsize=1), 
                zorder=4,
                color=color)
        
    ax.grid(True, zorder=3, axis="y")
    ax.set_xlabel('(b) List operations')
    ax.set_yscale("log")
    ax.set_xticks(x, nice_list_workload_names, fontsize="8")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('result_dir', 
                       help='Directory containing microbenchmark output data')
    parser.add_argument('-o', '--output',
                       default='figure2.pdf',
                       help='Output file for plot')
    parser.add_argument('-j', '--json',
                       default='results.json',
                       help='JSON file name')
    parser.add_argument('-r', '--read',
                        action='store_true',
                        default=False, 
                        help='Flag indicating whether program should read  \
                            results from a JSON file or compute and store them \
                            in the file. Default false (compute and store).')
    return parser.parse_args()

def plot(results, output_file):
    fig, axs = plt.subplots(1, 2, width_ratios=[2,1])
    fig.set_figwidth(10)
    fig.set_figheight(1.8)

    plot_results(axs[0], results)
    plot_list_results(axs[1], results)
    plt.tight_layout(pad=1)

    fig.legend(nice_kvstore_names, loc="upper center", fontsize="9", 
        ncol=4, bbox_to_anchor=(0.5, 1.07))    

    # Save the plot
    plt.savefig(output_file, bbox_inches="tight")
    print(f"Plot saved as '{output_file}'")
    plt.close()
    

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    if not args.read:
        # Process the data
        results = parse_files(args.result_dir)
        # Store the data
        save_results_to_json(results, args.json)
    else: 
        results = read_results_from_json(args.json)
    
    plot(results, args.output)

main()