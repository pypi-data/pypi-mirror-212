# The Lord of the rings API Python SDK

Welcome to this Python SDK repository for the The Lord of the rings API.

This is a simple library to facilitate the usage of the The Lord of the rings API.

Register on https://the-one-api.dev/ to get your API token used to authenticate your requests

## Installing the package from pypi

```
# create a virtual environment
>>> python3 -m venv venv
>>> pip install ayomide-sdk==0.0.7
```

## Installing the sdk client
```
>>> from ayomide_sdk.rest import Client
>>> client = Client(version="v2", api_key="API-KEY")
>>> quotes = client.quote.get()
>>> quotes["status"]
200
>>> quotes["json"]
{}
```

### for /movie
```
>>> from ayomide_sdk.rest import Client
>>> client = Client(version="v2", api_key="API-KEY")
>>> movies = client.quote.get()
>>> movies["status"]
200
>>> movies["json"]
{}
```

### for /movie/id
```
>>> from ayomide_sdk.rest import Client
>>> client = Client(version="v2", api_key="API-KEY")
>>> single_movie = client.movie.get(params={'id':"5cd95395de30eff6ebccde57"})
>>> single_movie["status"]
200
>>> single_movie["json"]
{}
```

### for /movie/id/quote
```
>>> from ayomide_sdk.rest import Client
>>> client = Client(version="v2", api_key="API-KEY")
>>> movie_quotes = client.quote.get(params={"id":"5cd95395de30eff6ebccde57","subquery"="quote"})
>>> movie_quotes["status"]
200
>>> movie_quotes["json"]
{}
```

### for /quote
```
>>> from ayomide_sdk.rest import Client
>>> client = Client(version="v2", api_key="API-KEY")
>>> quotes = client.quote.get(params={"id":"5cd95395de30eff6ebccde57","subquery"="quote"})
>>> quotes["status"]
200
>>> quotes["json"]
{}
```

### for /quote/id
```
>>> from ayomide_sdk.rest import Client
>>> client = Client(version="v2", api_key="API-KEY")
>>> single_quote = client.quote.get(params={'id':"5cd95395de30eff6ebccde57"})
>>> single_quote["status"]
200
>>> single_quote["json"]
{}
```

### for pagination filter (can be used for movie and quotes on any edpoints)
```
>>> from ayomide_sdk.rest import Client
>>> client = Client(version="v2", api_key="API-KEY")
>>> single_movie = client.movie.get(params={'id':"5cd95395de30eff6ebccde57"}, filters={"limit":"100","page":"2"})
>>> single_movie["status"]
200
>>> single_movie["json"]
{}
```


## Supported Python Versions
This library supports the following Python implementations:

Python 3.6
Python 3.7
Python 3.8
Python 3.9
Python 3.10

## Installation

ayomide_sdk is available on PyPI: 
```
python -m pip install ayomide_sdk
```

## More about ayomide_sdk

Read more <a href="https://github.com/Alsaheem/ayomide-sdk" target="_blank">here</a>
