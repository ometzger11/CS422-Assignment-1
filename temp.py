import geonamescache

gc = geonamescache.GeonamesCache(min_city_population=500)

site = "Ulaanbaatar"

print(gc.search_cities(site))
#print(gc.get_cities_by_name(site))
