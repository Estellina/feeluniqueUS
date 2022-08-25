#!/usr/bin/env python
"""Dictionary initializer.

Initializes the required dictionaries and returns them to data_collector.py."""

import time


def init_url_dict():
    url_dict = {
        'product_url': None,
        'n_reviews': None,
        'product_name': None,
        'product_price': None,
        'mean_rating': None
    }
    return url_dict


def init_product_dict():
    product_dict = {
        'product_name': None,
        'product_information': None,
        'mean_rating': None,
        'product_price': None,
        'n_reviews': None,
        'product_url': None
    }
    return product_dict


def init_reviews_dict():
    reviews_dict = {
        'review_rating': None,
        'review_title': None,
        'review_author': None,
        'review_date': None,
        'review_text': None,
        'collect_date': str(time.strftime("%Y_%m_%d"))
    }
    return reviews_dict
