import django
django.setup()
from bike_app.models import Bike
import scrapy
import locale
from scrapy_djangoitem import DjangoItem


class BikeItem(DjangoItem):
    django_model = Bike


class PropelSpider(scrapy.Spider):
    name = "propel"
    allowed_domains = ["propelbikes.com"]
    start_urls = [
        "http://propelbikes.com/bikes-by-price/2501-3500",
    ]

    def parse(self, response):
        models = response.xpath("//div[@class='name']/a/text()").extract()
        prices = response.xpath("//span[@class='price-fixed']/text()").extract()
        locale.setlocale(locale.LC_ALL, '')


        for i in range(len(models)):
            b = BikeItem()
            price = prices[i].strip('$')
            price = locale.atof(price[:])
            b['Model'] = models[i]
            b['Price'] = price
            bike = b.save()
            print bike.Model
            print bike.Price
