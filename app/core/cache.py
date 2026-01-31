from cachetools import TTLCache

people_list_cache = TTLCache(maxsize=100, ttl=60)     
person_cache = TTLCache(maxsize=500, ttl=300)
film_cache = TTLCache(maxsize=200, ttl=600)
planet_cache = TTLCache(maxsize=200, ttl=600)
species_cache = TTLCache(maxsize=200, ttl=600)

