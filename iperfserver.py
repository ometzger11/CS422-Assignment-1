import os
import json

# for distance calculation
import geonamescache
from geopy.distance import geodesic

# ping script name
SCRIPT = "./ping_server.sh"

# hardcoded purdue coords
PURDUE_COORDS = (40.4237, -86.9212)

# build a cache of cities for us to use to compute distance (lat and longitude provided)
gc = geonamescache.GeonamesCache(min_city_population=1000)

# represents an actual server with info from the JSON dump
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
        self.distance = self.distance_to_purdue()

        # stuff to find out for the assignment
        self.min_rtt = None
        self.max_rtt = None
        self.avg_rtt = None

    # runs the ping test for each server
    def run_ping(self):
        cmdline = SCRIPT + " " + self.host
        print("Pretending to run: " + cmdline)

        #os.system(cmdline)

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
            return 0.0

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

servers = parse_servers("listed_iperf3_servers.json")

count = 0
for server in servers:
    print(f"{count}: {server.str()}")
    count = count + 1

print("\n\n")

for server in servers:
    server.run_ping()
