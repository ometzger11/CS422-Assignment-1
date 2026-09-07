#!/bin/bash

# Responsible for pinging a single server and determining its stats
#
# Usage:
# ping_server.sh [ip_addr]

NPINGS=2

ping -c $NPINGS $1 > ping_results.txt

cat ping_results.txt | grep rtt | awk -F "=" '{print $2}'
