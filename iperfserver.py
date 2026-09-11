import os
import json

# for distance calculation
import geonamescache
from geopy.distance import geodesic

# for plot generation
import matplotlib.pyplot as plt

# ping script name
SCRIPT = "./ping_server.sh"

# hardcoded purdue coords
PURDUE_COORDS = (40.4237, -86.9212)

# build a cache of cities for us to use to compute distance (lat and longitude provided)
gc = geonamescache.GeonamesCache(min_city_population=1000)

# represents an actual server with info from the JSON dump
# if site is None, the location is assumed to be this machine (localhost)
class IperfServer:
    def __init__(self, host, port, options, gbps, continent, country, site, provider):
        self.host = host
        self.port = port
        self.options = options
        self.gbps = gbps
        self.continent = continent
        self.country = country
        self.site = site
        self.provider = provider

        if self.site is None:
            self.distance = 0.0
        else:
            self.distance = self.distance_to_purdue()

        # stuff to find out for the assignment
        self.min_rtt = None
        self.avg_rtt = None
        self.max_rtt = None

    # runs the ping test for each server
    def run_ping(self):
        cmdline = SCRIPT + " " + self.host
        print("\nAbout to run: " + cmdline)

        pipe = os.popen(cmdline)	

        line = pipe.readline()
        #print("Got: " + line)

        status = pipe.close()

        if status is not None:
            code = os.waitstatus_to_exitcode(status)
            raise RuntimeError(f"Script {SCRIPT} crashed with exit code {code}")

        parsed = json.loads(line)
        #print("Parsed: " + str(parsed))

        if "exitcode" in parsed:
            print(f"Ping failed for {self.host}")
        else:
            self.min_rtt = parsed["min"]
            self.avg_rtt = parsed["avg"]
            self.max_rtt = parsed["max"]

            print(f"Results for {self.host}")
            print(f"Minimum: {self.min_rtt}")
            print(f"Average: {self.avg_rtt}")
            print(f"Maximum: {self.max_rtt}")

    # helper for finding the distance in km from the server location to Purdue
    def distance_to_purdue(self):
        if not self.country or not self.site:
            raise ValueError(f"Error calculating distance on {self.host}: country or site undefined.")

        #print("Site: " + self.site)

        matches = gc.get_cities_by_name(self.site)
        #matches = gc.search_cities(self.site, contains_search=False)

        #print("Done")

        location = None

        for match in matches:
            city = next(iter(match.values()))
            #city = match

            if city["countrycode"].upper() == self.country.upper():
                location = city
                break

        if location is None:
            return None

        server_coords = (location["latitude"], location["longitude"])

        return geodesic(PURDUE_COORDS, server_coords).km

    def str(self):
        return f"{self.provider} - {self.site}, {self.country} ({self.host}:{self.port}). {self.distance} km away."

def parse_servers(filename):
    with open(filename, "r") as file:
        data = json.load(file)

    servers = []

    for entry in data:
        server = IperfServer(
            entry["IP/HOST"],
            entry["PORT"],
            entry["OPTIONS"],
            entry["GB/S"],
            entry["CONTINENT"],
            entry["COUNTRY"],
            entry["SITE"],
            entry["PROVIDER"]
        )

        servers.append(server)

    return servers

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
