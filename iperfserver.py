import json

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

    def str(self):
        return f"{self.provider} - {self.site}, {self.country} ({self.host}:{self.port})"

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

for server in servers:
    print(server.str())