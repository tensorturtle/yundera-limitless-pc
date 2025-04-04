#!/bin/bash
# disk_test_extended.sh - Extended disk performance tests with debugging
# This script performs sequential throughput tests (using dd) and random I/O tests (using fio).
# It outputs a JSON file with the results.
#
# Install `fio` and `bc` before running this script.
#
# Usage: ./disk_test_extended.sh "System Name"
# Example:
#   ./disk_test_extended.sh "VM with Local Storage"
#   
#
# Configuration for sequential tests using fio
SEQ_FILE="seq_test_file"
BS="1M"
SIZE="1G"
SEQ_OUTPUT_FILE="disk_test_extended_result.json"
SYSTEM_NAME=${1:-"Unknown System"}

echo "Running sequential tests on ${SYSTEM_NAME} using fio..."

# --- Sequential Write Test ---
echo "Starting sequential write test..."
SEQWRITE_JSON=$(fio --name=seqwrite --rw=write --ioengine=libaio --direct=1 --bs=$BS --size=$SIZE --numjobs=1 --group_reporting --output-format=json --filename=$SEQ_FILE)
# Extract sequential write bandwidth (in KB/s) then convert to MB/s.
SEQ_WRITE_BW_KB=$(echo "$SEQWRITE_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['jobs'][0]['write']['bw'])")
SEQ_WRITE_MB=$(echo "$SEQ_WRITE_BW_KB / 1024" | bc -l)
echo "Sequential write speed: ${SEQ_WRITE_MB} MB/s."

# --- Sequential Read Test ---
echo "Starting sequential read test..."
SEQREAD_JSON=$(fio --name=seqread --rw=read --ioengine=libaio --direct=1 --bs=$BS --size=$SIZE --numjobs=1 --group_reporting --output-format=json --filename=$SEQ_FILE)
SEQ_READ_BW_KB=$(echo "$SEQREAD_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['jobs'][0]['read']['bw'])")
SEQ_READ_MB=$(echo "$SEQ_READ_BW_KB / 1024" | bc -l)
echo "Sequential read speed: ${SEQ_READ_MB} MB/s."

# Remove the sequential test file
rm -f $SEQ_FILE

# --- Random I/O Tests using fio ---
if ! command -v fio >/dev/null 2>&1; then
    echo "fio is not installed. Skipping random I/O tests."
    RANDOM_WRITE_IOPS=0
    RANDOM_READ_IOPS=0
    RANDOM_WRITE_LAT=0
    RANDOM_READ_LAT=0
else
    echo "Running random I/O tests with fio..."

    # Random Write Test:
    RANDWRITE_JSON=$(fio --name=randwrite --ioengine=libaio --iodepth=32 --rw=randwrite --bs=4k \
        --direct=1 --size=100M --numjobs=1 --time_based --runtime=10 --group_reporting --output-format=json)
    RANDOM_WRITE_IOPS=$(echo "$RANDWRITE_JSON" | python3 -c "import sys, json; print(json.load(sys.stdin)['jobs'][0]['write']['iops'])")
    RANDOM_WRITE_LAT=$(echo "$RANDWRITE_JSON" | python3 -c "import sys, json; print(json.load(sys.stdin)['jobs'][0]['write']['lat_ns']['mean'] / 1e6)")

    # Random Read Test:
    RANDREAD_JSON=$(fio --name=randread --ioengine=libaio --iodepth=32 --rw=randread --bs=4k \
        --direct=1 --size=100M --numjobs=1 --time_based --runtime=10 --group_reporting --output-format=json)
    RANDOM_READ_IOPS=$(echo "$RANDREAD_JSON" | python3 -c "import sys, json; print(json.load(sys.stdin)['jobs'][0]['read']['iops'])")
    RANDOM_READ_LAT=$(echo "$RANDREAD_JSON" | python3 -c "import sys, json; print(json.load(sys.stdin)['jobs'][0]['read']['lat_ns']['mean'] / 1e6)")
    
    echo "Random write IOPS: ${RANDOM_WRITE_IOPS}, latency: ${RANDOM_WRITE_LAT} ms."
    echo "Random read IOPS: ${RANDOM_READ_IOPS}, latency: ${RANDOM_READ_LAT} ms."
fi

# Get current timestamp in ISO format
TIMESTAMP=$(date -Iseconds)

# Create JSON output with both sequential and random test results
cat <<EOF > $SEQ_OUTPUT_FILE
{
  "system": "$SYSTEM_NAME",
  "timestamp": "$TIMESTAMP",
  "sequential": {
    "write_MBps": $SEQ_WRITE_MB,
    "read_MBps": $SEQ_READ_MB
  },
  "random": {
    "write_IOPS": $RANDOM_WRITE_IOPS,
    "read_IOPS": $RANDOM_READ_IOPS,
    "write_latency_ms": $RANDOM_WRITE_LAT,
    "read_latency_ms": $RANDOM_READ_LAT
  }
}
EOF

echo "Extended disk test results saved to $SEQ_OUTPUT_FILE"

