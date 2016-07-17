import logging
from scrapy.exceptions import DropItem

class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    words_to_filter = ['politics', 'religion']

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if word in unicode(item['title']).lower():
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item

import pymongo
from scrapy.exceptions import DropItem

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
#MONGODB_DB = "stackoverflow"
#MONGODB_COLLECTION = "questions"
MONGODB_DB = "Blog"
MONGODB_COLLECTION = "popular"

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            MONGODB_SERVER,
            MONGODB_PORT
        )
        db = connection[MONGODB_DB]
        self.collection = db[MONGODB_COLLECTION]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            logging.log(logging.DEBUG, "Question added to MongoDB database!")
        return item


