import scrapy
#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurator.settings")
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)
from scrapy_djangoitem import DjangoItem
from decisions.models import Bike
# from Users.ransomv.Django_tutorial.examples.configurator.configurator.decisions.models

# import urlparse
# import unicodedata
# import string, csv, json


class Bikey(scrapy.Item):
    Model = scrapy.Field()
    Price = scrapy.Field()
    Best_Use = scrapy.Field()
    Range  = scrapy.Field()

class PropelSpider(scrapy.Spider):
    name = "propel1"
    allowed_domains = ["propelbikes.com"]
    start_urls = [
        "http://propelbikes.com/bikes-by-price/1501-2500",
    ]

    def parse(self, response):
        """ This gets all the bike model names """
        print "***** I am in parse function !!!!!"
        bikeModels = response.xpath('//*[@id="content"]/div[2]/div[3]/div/div[2]/a/text()').extract()
        bikePrices = response.xpath('//*[@id="content"]/div[2]/div[3]/div/div[4]/div/span[@class="price-fixed"]/text()').extract()
        # bikeModel = json.dumps(bikeModel)  # Get rid of the 'u'
        # bikePrice = json.dumps(bikePrice)
        print "!!!!! Value of bikeModel is: ", bikeModels
        print "Value of len(bikeModel is:)", len(bikeModels)
        print "Value of type(bikeModel is:)", type(bikeModels)
        print "!!!!! Value of bikePrice is: ", bikePrices
        for i, bikeModel in enumerate(bikeModels):
             # print bike
            # num = str(i)
            # cur_bike = "bike" + num
            # print "cur_bike is: ", cur_bike
            exec("bike%d = Bike()"%i)
            exec("bike%d['Model'] = bike" %i)
            new_bike = Bike()
            new_bike.Model = bikeModel
            new_bike.price = bikePrices[i]
            print "!!!!! new_bike.model is: ", new_bike.Model
            print "!!!!! new_bike.price is: ", new_bike.Price
            """ Tiffany's suggestions - import the models file """
            # new_bike.save()
       

        # print "bike%d is: "%i, "bike%d"%    i['Model']
        # print "bike1 is: ", bike1['Model']

        # test = Bike()
        # test['Model'] = 'Shwinn'
        # test['Price'] = '2500'
        # print "!!!!! Bike Model is: ", test['Model']
        # yield test
        # for i in range(len(table)):
        #   table.append(unicodedata.normalize('NFKD', table[i]).encode('ascii', 'ignore'))
        # print table
