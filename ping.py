import os
import json

# for distance calculation
import geonamescache
from geopy.distance import geodesic

# for plot generation
import matplotlib.pyplot as plt

# our shared utilities for parts 1 and 2
from server_utils import IperfServer, parse_servers

SCRIPT = "./ping_server.sh"

def run_ping(server):
    cmdline = SCRIPT + " " + server.host
    print("\nAbout to run: " + cmdline)
    pipe = os.popen(cmdline)
    line = pipe.readline()
    status = pipe.close()

    if status is not None:
        code = os.waitstatus_to_exitcode(status)
        raise RuntimeError(f"Script {SCRIPT} crashed with exit code {code}")

    parsed = json.loads(line)

    if "exitcode" in parsed:
        print(f"Ping failed for {server.host}")
    else:
        server.min_rtt = parsed["min"]
        server.avg_rtt = parsed["avg"]
        server.max_rtt = parsed["max"]
        print(f"Results for {server.host}: Min={server.min_rtt}, Avg={server.avg_rtt}, Max={server.max_rtt}")

local_server = IperfServer(
    "localhost",
    None,
    None,
    None,
    "North America",
    "US",
    None,
    None
)

servers = [local_server] + parse_servers("listed_iperf3_servers.json")

print("\nServer list:")

count = 0
for server in servers:
    print(f"{count}: {server.str()}")
    count = count + 1

print("\n\n")

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
    run_ping(server)

    # Servers without data due to failed ping (unreachable)
    if server.avg_rtt is None:
        print("No data for " + server.host)
        continue

    xvals.append(server.distance)
    yvals.append(server.avg_rtt)

    count += 1

plt.plot(xvals, yvals, 'bo')
plt.savefig("graph1.pdf")
