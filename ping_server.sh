#!/bin/bash

# Responsible for pinging a single server and determining its stats
#
# Usage:
# ping_server.sh [ip_addr]

NPINGS=4

ping -c $NPINGS $1 > ping_results.txt

line=$(cat ping_results.txt | grep rtt | awk -F "=" '{print $2}')

echo $line | awk -F "/" '{print $1}'
echo $line | awk -F "/" '{print $2}'
echo $line | awk -F "/" '{print $3}'
