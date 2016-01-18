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
    start_urls = ["http://propelbikes.com/bikes-by-price/2501-3500",
                  "http://propelbikes.com/bikes-by-price/3501-4500",
                  "http://propelbikes.com/bikes-by-price/1501-2500",
                  "http://propelbikes.com/bikes-by-price/more-than-4501"]

    def parse(self, response):
        models = response.xpath("//div[@class='name']/a/text()").extract()
        prices = response.xpath("//span[@class='price-fixed']/text()").extract()
        locale.setlocale(locale.LC_ALL, '')  # Convert unicode currency to decimal
        urls = response.xpath("//div[@class='name']/a/@href").extract()
        for i in range(len(models)):
            b = BikeItem()
            price = "%.2f" % locale.atof(prices[i].strip('$').replace(',', '')[:])
            b['model'] = models[i]
            b['price'] = price
            b['url'] = urls[i]
            if Bike.objects.filter(model=b['model']).exists():
                print 'bike model exists.  calling update_or_add'
                bike_record = Bike.objects.get(model=b['model'])
                check_bike = UpdateBike()
                detail_changes = check_bike.update_bike(bike_record, b)  # bike
                # record exists.  Updating price or url if changed
                print "Value of detail_changes is:  " + detail_changes
                continue
            b.save()

        for i in range(len(models)):
            b = BikeItem()
            b['model'] = models[i]
            yield scrapy.Request(urls[i], callback=self.parse_attr)

    def parse_attr(self, response):
        bike_dic = {}
        b = BikeItem()
        spec = SpecsItem()
        Url = response.url
        print "value of Url in parse_attr is:  " + Url
        spec["attr"] = response.xpath('//*[@id="tab-attribute"]/table/tbody/tr\
            /td/text()').extract()
        bike_dic = dict(map(None, *[iter(spec["attr"])]*2))  
        # Converts list spec["attr"] to dict
        b = Bike.objects.get(url=Url)
        print "Value of b.url is: " + b.url
        b_range = filter(str.isdigit, bike_dic["Range"]\
            .encode('ascii', 'ignore'))
        best_use = bike_dic["Best Use"]
        assistance = bike_dic["Assistance"]
        motor = bike_dic["Motor"]
        top_speed = bike_dic["Top Speed"]
        top_speed = max(map(float, re.findall(r'\d*\.?\d+', top_speed)))
        if "Weight" in bike_dic:
            weight = map(float, re.findall(r'\d*\.?\d+', bike_dic["Weight"]))[0]
            b.weight = weight
        brakes = bike_dic["Brakes"].rstrip('\r+\n')
        battery = bike_dic["Battery"]
        battery = battery.replace(',', '')  # get rid of any #'s with commas
        battery = re.findall(r'\d*\.?\d+\s*[A,a,V,v,WH,Wh,wH,wh]+', battery)
        bat = []
        print " !!! Value of battery is  !!!", battery
        for i in range(len(battery)):
            if (i > 0) & ('v' in battery[i].lower()):  # save only 1st set of
                break                                  # battery values
            bat.append(battery[i])
        battery = bat
        b.b_range = b_range
        b.best_use = best_use
        b.assistance = assistance
        b.motor = motor
        b.top_speed = top_speed
        b.brakes = brakes
        if battery:  # Only populate field if relevent info exists
            battery = [str(x) for x in battery]  # conv unicode to ascii
            battery = [x.replace(' ', '') for x in battery]  # get rid of spaces
            b.battery = ' '.join(battery).upper()  # convert list to string
        b.photo = response.xpath('//*[@id="content"]/div[3]/div[1]/div[1]/\
            div[1]/a/img/@src').extract()
        # These if's are necessary for the 4 cases which xpath to photos isn't
        # in the expected location
        if not b.photo:
            b.photo = response.xpath('//*[@id="content"]/div[4]/div[1]/div[1]\
                /div/a/img/@src').extract()
            if not b.photo:
                b.photo = response.xpath('//*[@id="content"]/div/div[1]/div[1]\
                    /div/a/@href').extract()
                print "!!! b.photo and Url for felt bike is: "
                print b.photo
                print Url
        b.photo = b.photo[0].encode("ascii", "ignore")
        b.save()


class UpdateBike():

    def update_bike(self, bike_record, b):
        if bike_record.price != b['price']:
            print "!!!! price has changed.  updating price !!!!"
            bike_record.price = b['price']
            bike_record.save()
        if bike_record.url != b['url']:
            print "!!!! url has changed.  updating url !!!!"
            bike_record.url = b['url']
            bike_record.save()
        return 'done with update_or_add'
