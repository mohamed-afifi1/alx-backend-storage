#!/usr/bin/env python3
"""
update in school
"""


def update_topics(mongo_collection, name, topics):
    """
    Update the topics of a student in the school
    """
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
