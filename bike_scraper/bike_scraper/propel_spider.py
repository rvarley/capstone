import django
django.setup()
from bike_app.models import Bike
import scrapy
from scrapy_djangoitem import DjangoItem
import locale

bike_dic = {}


class BikeItem(DjangoItem):
    django_model = Bike


class SpecsItem(scrapy.Item):
    link = scrapy.Field()
    attr = scrapy.Field()


class PropelSpider(scrapy.Spider):
    name = "propel"
    allowed_domains = ["propelbikes.com"]
    # start_urls = ["http://propelbikes.com/bikes-by-price/3501-4500",]
    start_urls = ["http://propelbikes.com/bikes-by-price/more-than-4501",
                  "http://propelbikes.com/bikes-by-price/3501-4500",
                  "http://propelbikes.com/bikes-by-price/2501-3500",
                  "http://propelbikes.com/bikes-by-price/1501-2500",
    ]

    def parse(self, response):
        global bike_dic
        models = response.xpath("//div[@class='name']/a/text()").extract()
        prices = response.xpath("//span[@class='price-fixed']/text()").extract()
        locale.setlocale(locale.LC_ALL, '')
        urls = response.xpath("//div[@class='name']/a/@href").extract()

        for i in range(len(models)):
            b = BikeItem()
            price = prices[i].strip('$')
            price = locale.atof(price[:])
            b['model'] = models[i]
            b['price'] = price
            b['url'] = urls[i]
            b.save()

        for i in range(len(models)):
            b = BikeItem()
            b['model'] = models[i]
            yield scrapy.Request(urls[i], callback=self.parse_attr)

    def parse_attr(self, response):
        global bike_dic
        b = BikeItem()
        spec = SpecsItem()
        Url = response.url
        spec["attr"] = response.xpath('//*[@id="tab-attribute"]/table/tbody/tr/td/text()').extract()
        bike_dic = dict(map(None, *[iter(spec["attr"])]*2))  # Converts list spec["attr"] to dict
        b = Bike.objects.get(url=Url)
        # range = [int(s) for s in bike_dic["Range"].split() if s.isdigit()][0]
        range = filter(str.isdigit, bike_dic["Range"].encode('ascii', 'ignore'))
        # getting int range out of string
        b.b_range = range
        print "!!! b.b_range and b.model are: "
        print b.b_range, b.model
        b.save()
