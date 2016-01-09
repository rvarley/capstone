import django
django.setup()
from bike_app.models import Bike
import scrapy
from scrapy_djangoitem import DjangoItem
import locale
import re


class BikeItem(DjangoItem):
    django_model = Bike


class SpecsItem(scrapy.Item):
    link = scrapy.Field()
    attr = scrapy.Field()


class PropelSpider(scrapy.Spider):
    name = "propel"
    allowed_domains = ["propelbikes.com"]
    start_urls = ["http://propelbikes.com/bikes-by-price/more-than-4501",
                  "http://propelbikes.com/bikes-by-price/3501-4500",
                  "http://propelbikes.com/bikes-by-price/2501-3500",
                  "http://propelbikes.com/bikes-by-price/1501-2500"]

    def parse(self, response):
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
            if Bike.objects.filter(model=b['model']).exists():
                print "!!! Bike exists, doing nothing !!!"
                print b['model']
                continue
            b.save()
        for i in range(len(models)):
            b = BikeItem()
            b['model'] = models[i]
            if Bike.objects.filter(model=b['model']).exists():
                print "!!! Bike exists, doing nothing !!!"
                print b['model']
                continue
            yield scrapy.Request(urls[i], callback=self.parse_attr)

    def parse_attr(self, response):
        bike_dic = {}
        b = BikeItem()
        spec = SpecsItem()
        Url = response.url
        spec["attr"] = response.xpath('//*[@id="tab-attribute"]/table/tbody/tr/td/text()').extract()
        bike_dic = dict(map(None, *[iter(spec["attr"])]*2))  # Converts list spec["attr"] to dict
        b = Bike.objects.get(url=Url)
        b_range = filter(str.isdigit, bike_dic["Range"].encode('ascii', 'ignore'))
        best_use = bike_dic["Best Use"]
        assistance = bike_dic["Assistance"]
        motor = bike_dic["Motor"]
        top_speed = bike_dic["Top Speed"]
        top_speed = max(map(float, re.findall(r'\d*\.?\d+', top_speed)))
        if "Weight" in bike_dic:
            weight = bike_dic["Weight"]
            b.weight = weight
        brakes = bike_dic["Brakes"].rstrip('\r+\n')
        battery = bike_dic["Battery"]
        b.b_range = b_range
        b.best_use = best_use
        b.assistance = assistance
        b.motor = motor
        b.top_speed = top_speed
        b.brakes = brakes
        b.battery = battery
        b.photo = response.xpath('//*[@id="content"]/div[3]/div[1]/div[1]/div[1]/a/img/@src').extract()
        # These if's are necessary for 4 cases which xpath to photos isn't
        # in the usual place.
        if not b.photo:
            b.photo = response.xpath('//*[@id="content"]/div[4]/div[1]/div[1]/div/a/img/@src').extract()
            if not b.photo:
                b.photo = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div/a/@href').extract()
                print "!!! b.photo and Url for felt bike is: "
                print b.photo
                print Url
        b.photo = b.photo[0].encode("ascii", "ignore")
        b.save()
