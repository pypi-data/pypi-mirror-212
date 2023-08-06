"""
This file is used to store helper functions across the application
"""


def full_url_query_builder(base_url, api_type):
    return base_url + f"/{api_type}"


def build_filters(filters):
    filter_query = "?"
    for k, v in filters.items():
        filter_query = filter_query + f"{k}={v}&"
    return filter_query[:-1]  # remove trailing &
