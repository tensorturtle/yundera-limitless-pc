# Yundera Limitless PC

[**Read the full report**](/REPORT.md)
[**Read the full setup documentation**](/SETUP.md)

### Executive Summary

This report outlines the successful development of a proof-of-concept VM that enables **zero-downtime vertical scaling of virtual machines**, a feature currently unavailable on mainstream cloud platforms. Built for Yundera’s user-centric model, the solution leverages open-source technologies (**Proxmox VE** for virtualization and **Ceph** for distributed storage) deployed on bare-metal servers from Scaleway.

The proof of concept demonstrates that computing resources such as CPU, memory, and storage can be dynamically scaled without interrupting user workloads, paving the way for a "limitless PC" experience. Key advantages include lower vendor lock-in, cost-efficiency, and operational flexibility. The project also shows that live migration across servers is not only viable but nearly imperceptible to users.

Based on these findings, the report recommends progressing toward production by implementing infrastructure-as-code, usage-based billing, and enhanced security measures. This positions Yundera to offer a unique, scalable alternative to traditional cloud computing.
Infrastructure as Code and scripts for Yundera Limitless PC Project

## Subdirectories

+ [ansible](/ansible): To be run immediately after fresh install of Debian 11 on rented servers to set up Proxmox.
+ [backblaze-mount](/backblaze-mount): An example script that mounts Backblaze B2 buckets to the file system. To be used upon the first boot of a VM.
+ [performance-measurement](/performance-measurement): Bash scripts and python code that was used to measure system performance and produce graphs for the report.
