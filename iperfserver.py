import os
import json

# for distance calculation
import geonamescache
from geopy.distance import geodesic

# for plot generation
import matplotlib.pyplot as plt

# our shared utilities for parts 1 and 2
from server_utils import IperfServer, parse_servers

local_server = IperfServer(
    "localhostasdfsdf.biz",
    None,
    None,
    None,
    "North America",
    "US",
    None,
    None
)

servers = [local_server] + parse_servers("listed_iperf3_servers.json")

count = 0
for server in servers:
    print(f"{count}: {server.str()}")
    count = count + 1

print("\n\n")

"""
foobar = IperfServer(
    "google.com",
    5201,
    "-R",
    10,
    "North America",
    "US",
    "San Francisco",
    "DATAPACKET"
)

baz = IperfServer(
    "doesntexist.biz",
    5201,
    "-R",
    10,
    "Europe",
    "DE",
    "Hamburg",
    "DATAPACKET"
)

foobar.run_ping()
baz.run_ping()
"""

plt.xlabel("Distance (km)")
plt.ylabel("Average RTT (ms)")

xvals = []
yvals = []

earlycutoff = 8

count = 0
for server in servers:
    if count >= earlycutoff:
        break

    # Servers skipped due to lack of geolocation data (bad city name)
    if server.distance is None:
        print("\nSkipping " + server.host)
        continue

    # Run ping test right now (synchronous)
    server.run_ping()

    # Servers without data due to failed ping (unreachable)
    if server.avg_rtt is None:
        print("No data for " + server.host)
        continue

    xvals.append(server.distance)
    yvals.append(server.avg_rtt)

    count += 1

plt.plot(xvals, yvals, 'bo')
plt.savefig("graph1.pdf")
