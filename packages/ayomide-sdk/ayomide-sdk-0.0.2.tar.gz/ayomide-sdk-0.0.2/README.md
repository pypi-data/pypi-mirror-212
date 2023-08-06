from ayomide_sdk.rest import Client
client = Client(version="v2", api_key="ltLgmBHmMRdwJkE0zWFm")
client.quote.get()
client.movie.get()
client.movie.get(params={'id':"5cd95395de30eff6ebccde57"})

https://the-one-api.dev/v2/movie/5cd95395de30eff6ebccde5d/quote?

client.movie.get(params={'id':'5cd95395de30eff6ebccde5d','subquery':'quote'},filters={"limit":"100","page":"2"})