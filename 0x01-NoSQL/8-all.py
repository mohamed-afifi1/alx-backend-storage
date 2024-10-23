#!/usr/bin/env python3
"""
list all mongo doc in the input
"""


def list_all(mongo_collection):
    """
    List all documents in the given MongoDB collection.
    """
    obj = mongo_collection.find()
    return list(obj)
