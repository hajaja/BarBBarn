from scrapy.item import Item, Field

class Website(Item):
    name = Field()
    description = Field()
    url = Field()

class News(Item):
    title = Field()
    text = Field()
    url = Field()
    source = Field()
    dtCrawled = Field()
    dtCreated = Field()

class Blog(Item):
    source = Field()
    author = Field()
    dtCreated = Field()
    title = Field()
    text = Field()
    numRead = Field()
    numComment = Field()
    url = Field()
