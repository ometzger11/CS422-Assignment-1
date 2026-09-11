# This is a utility module that contains IperfServer class and parse_servers() function, needed for part 2

import json
import geonamescache
from geopy.distance import geodesic

PURDUE_COORDS = (40.4237, -86.9212)

print("Generating geocache...")
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
