# This is a utility module that contains IperfServer class and parse_servers() function, needed for part 2

import os
import json
import geonamescache
from geopy.distance import geodesic

SCRIPT = "./ping_server.sh"
PURDUE_COORDS = (40.4237, -86.9212)
gc = geonamescache.GeonamesCache(min_city_population=1000)

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

        self.min_rtt = None
        self.avg_rtt = None
        self.max_rtt = None

    def run_ping(self):
        cmdline = SCRIPT + " " + self.host
        print("\nAbout to run: " + cmdline)
        pipe = os.popen(cmdline)
        line = pipe.readline()
        status = pipe.close()

        if status is not None:
            code = os.waitstatus_to_exitcode(status)
            raise RuntimeError(f"Script {SCRIPT} crashed with exit code {code}")

        parsed = json.loads(line)

        if "exitcode" in parsed:
            print(f"Ping failed for {self.host}")
        else:
            self.min_rtt = parsed["min"]
            self.avg_rtt = parsed["avg"]
            self.max_rtt = parsed["max"]
            print(f"Results for {self.host}: Min={self.min_rtt}, Avg={self.avg_rtt}, Max={self.max_rtt}")

    def distance_to_purdue(self):
        if not self.country or not self.site:
            return None

        matches = gc.get_cities_by_name(self.site)
        location = None

        for match in matches:
            city = next(iter(match.values()))
            if city["countrycode"].upper() == self.country.upper():
                location = city
                break

        if location is None:
            return None

        server_coords = (location["latitude"], location["longitude"])
        return geodesic(PURDUE_COORDS, server_coords).km

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