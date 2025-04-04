#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
"""
compare_results_extended.py - Combines extended disk test JSON results from four systems
and outputs a PNG with comparison diagrams.
Usage: python compare_results_extended.py file1.json file2.json file3.json file4.json [--output comparison.png]
"""

import json
import argparse
import matplotlib.pyplot as plt
import numpy as np

def load_results(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def safe_get(d, keys, default='Not Available'):
    try:
        for key in keys:
            d = d[key]
        return float(d)
    except (KeyError, TypeError, ValueError):
        return default

def main():
    parser = argparse.ArgumentParser(description="Compare extended disk performance results from four systems.")
    parser.add_argument('files', nargs=4, help='JSON result files for the four systems')
    parser.add_argument('--output', default='comparison.png', help='Output PNG file name')
    args = parser.parse_args()

    results = [load_results(f) for f in args.files]
    systems = [r.get("system", f"System {i+1}") for i, r in enumerate(results)]
    colors = ['salmon', 'greenyellow', 'darkturquoise', 'plum']

    seq_metrics = ['Write', 'Read']
    rand_metrics = ['Write', 'Read']
    x = np.arange(len(seq_metrics))
    bar_width = 0.18

    # Collect data
    seq_values = [[safe_get(r, ["sequential", "write_MBps"]),
                   safe_get(r, ["sequential", "read_MBps"])] for r in results]

    rand_iops = [[safe_get(r, ["random", "write_IOPS"]),
                  safe_get(r, ["random", "read_IOPS"])] for r in results]

    rand_latency = [[safe_get(r, ["random", "write_latency_ms"]),
                     safe_get(r, ["random", "read_latency_ms"])] for r in results]

    fig, axs = plt.subplots(3, 1, figsize=(10, 14))

    # Plot helper
    def plot_metric(ax, title, values, ylabel):
        for i in range(4):
            offset = (i - 1.5) * bar_width
            bars = []
            for j in range(len(values[i])):
                val = values[i][j]
                if isinstance(val, float):
                    bars.append(val)
                else:
                    bars.append(0)  # Placeholder for missing data
            bar_container = ax.bar(x + offset, bars, bar_width, label=systems[i], color=colors[i])
            for j, val in enumerate(values[i]):
                if not isinstance(val, float):
                    ax.text(x[j] + offset, 1, 'Not Available', ha='center', va='bottom', rotation=90, fontsize=8, color='red')

        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(seq_metrics)
        ax.set_ylabel(ylabel)
        ax.legend()

    plot_metric(axs[0], 'Sequential Throughput (MB/s)', seq_values, 'MB/s')
    plot_metric(axs[1], 'Random IOPS', rand_iops, 'IOPS')
    plot_metric(axs[2], 'Random Latency (ms)', rand_latency, 'ms')

    plt.tight_layout()
    plt.savefig(args.output)
    print(f"Comparison chart saved to {args.output}")

if __name__ == '__main__':
    main()

