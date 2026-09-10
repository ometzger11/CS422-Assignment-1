#!/bin/bash

# Responsible for pinging a single server and determining its stats
#
# Usage:
# ping_server.sh [ip_addr]

NPINGS=4

ping -c $NPINGS $1 > ping_results.txt

line=$(cat ping_results.txt | grep rtt | awk -F "=" '{print $2}')

min=$(echo $line | awk -F "/" '{print $1}')
avg=$(echo $line | awk -F "/" '{print $2}')
max=$(echo $line | awk -F "/" '{print $3}')

echo "{\"min\": $min, \"avg\": $avg, \"max\": $max}"
