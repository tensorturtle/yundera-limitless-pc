# Throwaway Scripts for Performance Measurement & Visualization

Created with ChatGPT o3-mini-high.

We use [uv](https://astral.sh/uv) to run python scripts. This allows us to define dependencies within the file and run it standalone, without interference with system python or bothering with virtual environments.

## Inter-node Network Performance Ping & Throughput

Edit `network.py` with the server node information.

```
uv run network.py
```

## Disk Performance

We measure disk performance for four setups:

+ Native Host: SSH into the Proxmox host
+ VM (Local Drive): Create a VM that uses the host's local drive as the backing storage.
+ VM (Ceph): Create a VM that uses the Ceph cluster storage
+ VM (Backblaze): We mount a Backblaze B2 bucket on a VM and run the disk performance measurement on that directory.

In each case, we SSH into the relevant system / directory and run:

```
./disk_test_extended.sh NAME /TARGET/DIRECTORY
```

And then somehow get the resulting .json files together into the developer system, and then run:

```
uv run compare_disk_results.py
```

This outputs a .png of graphs.


