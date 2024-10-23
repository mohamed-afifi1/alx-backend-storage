#!/usr/bin/env python3
"""
add to the school
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new school document into the given MongoDB collection.
    """
    return mongo_collection.insert_one(kwargs).inserted_id
