#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
import subprocess
import json
import threading
import time
import re
import matplotlib.pyplot as plt
import numpy as np

# Define your server nodes.
nodes = [
    {"name": "node0", "hostname": "163.172.68.57", "user": "root", "key": "~/.ssh/yundera-poc"},
    {"name": "node1", "hostname": "163.172.68.59", "user": "root", "key": "~/.ssh/yundera-poc"},
    {"name": "node2", "hostname": "163.172.68.106", "user": "root", "key": "~/.ssh/yundera-poc"}
]

# Use the RdYlGn diverging colormap.
# For ping: reverse so that 0ms (green) to 10ms (red).
ping_cmap = plt.get_cmap("RdYlGn_r")
# For throughput: 0Mbps (red) to 1000Mbps (green) using RdYlGn.
throughput_cmap = plt.get_cmap("RdYlGn")

def run_remote_command(node, command):
    """
    Runs a command on a remote server via SSH.
    Returns the command's stdout as a string.
    """
    ssh_cmd = [
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-i", node["key"],
        f"{node['user']}@{node['hostname']}",
        command
    ]
    try:
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command on {node['name']}: {command}")
        print(e.stderr)
        raise

def ping_test(source_node, target_node):
    """
    Runs ping from source_node to target_node and returns the average round-trip time in ms.
    If source_node == target_node, uses loopback (127.0.0.1) to test self performance.
    """
    if source_node == target_node:
        cmd = "ping -c 4 127.0.0.1"
        print(f"Self ping test on {source_node['name']}...")
    else:
        cmd = f"ping -c 4 {target_node['hostname']}"
        print(f"Pinging from {source_node['name']} to {target_node['name']}...")
    output = run_remote_command(source_node, cmd)
    # Look for a line like: rtt min/avg/max/mdev = 1.234/2.345/3.456/0.123 ms
    m = re.search(r"rtt .* = ([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+) ms", output)
    if m:
        avg_ping = float(m.group(2))
        if source_node == target_node:
            print(f"Self ping on {source_node['name']}: {avg_ping} ms")
        else:
            print(f"Average ping from {source_node['name']} to {target_node['name']}: {avg_ping} ms")
        return avg_ping
    else:
        print(f"Could not parse ping output on {source_node['name']} (target: {target_node['name']}).")
        return np.nan

def run_iperf_server(node):
    """
    Runs iperf3 in server mode (with -1 so it exits after one connection)
    on the given node. This function is designed to be run in a thread.
    """
    cmd = "iperf3 -s -1"
    try:
        run_remote_command(node, cmd)
    except Exception as e:
        print(f"Error running iperf server on {node['name']}: {e}")

def iperf_test(server_node, client_node):
    """
    Runs an iperf3 test with server_node as server and client_node as client.
    Returns the measured throughput (from the server's perspective) in Mbps.
    If server_node == client_node, uses the loopback interface.
    """
    if server_node == client_node:
        ip_address = "127.0.0.1"
        print(f"Self iperf test on {server_node['name']}...")
    else:
        ip_address = server_node["hostname"]
        print(f"Running iperf3 test: server={server_node['name']} ({server_node['hostname']})  client={client_node['name']} ({client_node['hostname']})")
    # Start iperf3 server on server_node in a separate thread.
    server_thread = threading.Thread(target=run_iperf_server, args=(server_node,))
    server_thread.start()
    # Allow a moment for the server to initialize.
    time.sleep(1)
    # Run the iperf3 client on client_node with JSON output.
    client_cmd = f"iperf3 -c {ip_address} -t 5 -J"
    output = run_remote_command(client_node, client_cmd)
    server_thread.join(timeout=10)
    try:
        result = json.loads(output)
        bps = result["end"]["sum_received"]["bits_per_second"]
        mbps = bps / 1e6
        if server_node == client_node:
            print(f"Self iperf on {server_node['name']}: {mbps:.2f} Mbps")
        else:
            print(f"Throughput from {client_node['name']} to {server_node['name']}: {mbps:.2f} Mbps")
        return mbps
    except Exception as e:
        print(f"Error parsing iperf3 JSON output on {client_node['name']} (server: {server_node['name']}): {e}")
        return np.nan

def plot_matrix(matrix, title, filename, value_format="{:.2f}", unit="", vmin=None, vmax=None, cmap="viridis"):
    """
    Plots a heatmap matrix with annotations and saves it as a PNG.
    """
    fig, ax = plt.subplots()
    # Use a masked array to handle any NaN values.
    masked_matrix = np.ma.masked_invalid(matrix)
    cax = ax.imshow(masked_matrix, interpolation="nearest", cmap=cmap, vmin=vmin, vmax=vmax)
    plt.title(title)
    plt.colorbar(cax)
    ticks = np.arange(len(nodes))
    labels = [node["name"] for node in nodes]
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    # Annotate each cell with the measured value.
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            val = matrix[i, j]
            text = ""
            if not np.isnan(val):
                text = value_format.format(val) + unit
            ax.text(j, i, text, ha="center", va="center", color="w")
    plt.savefig(filename)
    plt.close()
    print(f"Saved {title} matrix to {filename}")

def main():
    num_nodes = len(nodes)
    # Create matrices for ping and iperf.
    ping_matrix = np.full((num_nodes, num_nodes), np.nan)
    iperf_matrix = np.full((num_nodes, num_nodes), np.nan)

    # Run ping tests for all pairs, including self-tests.
    print("Starting ping tests...")
    for i in range(num_nodes):
        for j in range(num_nodes):
            try:
                ping_matrix[i, j] = ping_test(nodes[i], nodes[j])
            except Exception as e:
                print(f"Ping test on {nodes[i]['name']} (target: {nodes[j]['name']}) failed: {e}")

    # Run iperf tests for all pairs, including self-tests.
    print("Starting iperf3 tests...")
    for i in range(num_nodes):
        for j in range(num_nodes):
            try:
                iperf_matrix[i, j] = iperf_test(nodes[i], nodes[j])
            except Exception as e:
                print(f"iperf3 test (server: {nodes[i]['name']}, client: {nodes[j]['name']}) failed: {e}")

    # Plot and save the matrices as PNG images.
    plot_matrix(ping_matrix, "Ping Times (ms)", "ping_matrix.png", value_format="{:.2f}", unit=" ms",
                vmin=0, vmax=10, cmap=ping_cmap)
    plot_matrix(iperf_matrix, "iperf3 Throughput (Mbps)", "iperf_matrix.png", value_format="{:.2f}", unit=" Mbps",
                vmin=0, vmax=1000, cmap=throughput_cmap)

if __name__ == "__main__":
    main()

