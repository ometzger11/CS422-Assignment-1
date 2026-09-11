#!/bin/bash

# Responsible for pinging a single server and determining its stats
#
# Usage:
# ping_server.sh [ip_addr]

#NPINGS=10
NPINGS=2

output=$(ping -c $NPINGS $1)
retval=$?

#echo "Status: $retval"
#echo "$output"

if [ $retval -ne 0 ]; then
	echo "{\"exitcode\": $retval}"
	exit
fi

line=$(echo "$output" | grep rtt | awk -F "=" '{print $2}')

min=$(echo $line | awk -F "/" '{print $1}')
avg=$(echo $line | awk -F "/" '{print $2}')
max=$(echo $line | awk -F "/" '{print $3}')

echo "{\"min\": $min, \"avg\": $avg, \"max\": $max}"
