import random
import matplotlib.pyplot as plt
import numpy as np
from server_utils import parse_servers
from traceroute_analysis import run_traceroute, parse_traceroute

# get server list
servers = parse_servers("listed_iperf3_servers.json")

# pick 5 randoms from the list
valid_servers = []
for s in servers:
    if s.distance is not None:
        valid_servers.append(s)

chosen = random.sample(valid_servers, 5)

# contains all data
all_hops = {}
hop_counts = []
total_rtts = []

# run traceroute on each
for server in chosen:
    print(f"\nTraceroute to {server.host}...")
    output = run_traceroute(server.host)
    
    if output:
        hops = parse_traceroute(output)
        all_hops[server.host] = hops
        
        # sum rtts to get total
        rtt_values = []
        for _, rtt in hops:
            if rtt is not None:
                rtt_values.append(rtt)
        total_rtt = sum(rtt_values)
        
        hop_count = 0
        for h, r in hops:
            if r is not None:
                hop_count += 1

        hop_counts.append(hop_count)
        total_rtts.append(total_rtt)
        
        print(f"  Hops: {hop_count}, Total RTT: {total_rtt:.2f}ms")

# start of plot 1 (bar chart)
fig, ax = plt.subplots(figsize=(12, 12))

servers_list = list(all_hops.keys())
x_pos = np.arange(len(servers_list))
bottoms = np.zeros(len(servers_list))

# find the max hop count out of every server
max_hops = 0
for hops in all_hops.values():
    max_hop_num = 0
    for h, r in hops:
        if h > max_hop_num:
            max_hop_num = h
    if max_hop_num > max_hops:
        max_hops = max_hop_num

# make the hops different colors
for hop_num in range(1, max_hops + 1):
    hop_rtts = []
    for server in servers_list:
        hops = all_hops[server]
        hop_data = []
        for h, rtt in hops:
            if h == hop_num and rtt is not None:
                hop_data.append(rtt)
        
        if hop_data:
            hop_rtts.append(hop_data[0])
        else:
            hop_rtts.append(0)
    # only plot if data is present
    if any(hop_rtts): 
        ax.bar(x_pos, hop_rtts, bottom=bottoms, label=f'Hop {hop_num}')
        bottoms += hop_rtts

ax.set_ylabel('RTT (ms)')
ax.set_xlabel('Server')
ax.set_title('Latency Breakdown by Hop')
ax.set_xticks(x_pos)
ax.set_ylim(0, max(bottoms) * 1.1) # adds 10% padding to the top
ax.set_xticklabels(servers_list, rotation=45, ha='right')
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig('hop_breakdown.pdf')
print("\nPlot saved: hop_breakdown.pdf")

# start of plot 2 (scatter chart)
plt.figure(figsize=(10, 6))
plt.scatter(hop_counts, total_rtts, s=100, alpha=0.6)
plt.xlabel('Hop Count')
plt.ylabel('Total RTT (ms)')
plt.title('Hop Count vs Round-Trip Time')
plt.grid(True)
plt.savefig('hopcount_vs_rtt.pdf')
print("Plot saved: hopcount_vs_rtt.pdf")