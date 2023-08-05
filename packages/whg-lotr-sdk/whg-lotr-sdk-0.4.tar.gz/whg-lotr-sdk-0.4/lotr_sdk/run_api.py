from lotr_sdk.sdk import LotrSdk
from pprint import pprint

sdk = LotrSdk()

r = sdk.movie.get_all(limit=5)

pprint(r)

r = sdk.movie.get_by_id('5cd95395de30eff6ebccde5d')

pprint(r)

r = sdk.quote.get_by_id('5cd96e05de30eff6ebcce7e9')

pprint(r)

r = sdk.quote.get_all(filter_string="character=5cd99d4bde30eff6ebccfe9e")

pprint(r)

r = sdk.quote.get_by_movie_id('5cd95395de30eff6ebccde5d')

pprint(r)

r = sdk.quote.get_by_movie_id('5cd95395de30eff6ebccde5d', limit=5, page=2)

pprint(r)