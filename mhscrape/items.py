# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MhscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Monster(scrapy.Item):
    en_name = scrapy.Field()
    jp_name = scrapy.Field()
    en_title = scrapy.Field()
    monster_class = scrapy.Field()
    elements = scrapy.Field()
    ailments = scrapy.Field()
    weakest_to_elements = scrapy.Field()
    habitats = scrapy.Field()
    generation = scrapy.Field()
    physiology_desc = scrapy.Field()
    abilities_desc = scrapy.Field()
    behavior_desc = scrapy.Field()
    habitat_desc = scrapy.Field()
