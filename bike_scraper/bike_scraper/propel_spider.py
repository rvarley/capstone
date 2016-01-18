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
    """ Create a container to hold scraped data """
    attr = scrapy.Field()


class PropelSpider(scrapy.Spider):
    """
    Spider to gather data from proplebikes.com website by all price point
    categories.
    """

    name = "propel"
    allowed_domains = ["propelbikes.com"]
    start_urls = ["http://propelbikes.com/bikes-by-price/2501-3500",
                  "http://propelbikes.com/bikes-by-price/3501-4500",
                  "http://propelbikes.com/bikes-by-price/1501-2500",
                  "http://propelbikes.com/bikes-by-price/more-than-4501"]

    def parse(self, response):
        """
        parse method scrapes fields for model price and URL which are all
        located on one page.  Data is saved to these 3 postgres fields.
        It then calls the parse_attr method with each bike model URL to
        gather specification on each scraped bike model.
        """

        models = response.xpath("//div[@class='name']/a/text()").extract()
        prices = response.xpath("//span[@class='price-fixed']/text()").extract()
        locale.setlocale(locale.LC_ALL, '')  # Convert unicode currency
                                             # to decimal
        urls = response.xpath("//div[@class='name']/a/@href").extract()
        for i, model in enumerate(models):
            b = BikeItem()
            price = "{0:.2f}".format(locale.atof(prices[i].strip('$')
                    .replace(',', '')))
            b['model'] = models[i]
            b['price'] = price
            b['url'] = urls[i]
            if Bike.objects.filter(model=b['model']).exists():
                bike_record = Bike.objects.get(model=b['model'])
                check_bike = UpdateBike()
                check_bike.update_bike(bike_record, b)  # bike
                # record exists.  Updating price or url if changed
                continue
            b.save()

        for i, model in enumerate(models):
            b = BikeItem()
            b['model'] = models[i]
            yield scrapy.Request(urls[i], callback=self.parse_attr)

    @staticmethod
    def parse_attr(response):
        """
        parse_attr method scrapes specifications for each bike model and saves
        them to the appropriate postgres bike_app_bike record using existing
        url field to determine which record to save the additional
        data to.
        """

        bike_dic = {}
        b = BikeItem()
        spec = SpecsItem()
        url = response.url
        spec["attr"] = response.xpath('//*[@id="tab-attribute"]/table/tbody/tr\
            /td/text()').extract()
        bike_dic = dict(map(None, *[iter(spec["attr"])]*2))
        # Converts list spec["attr"] to dict
        b = Bike.objects.get(url=url)
        b_range = filter(str.isdigit, bike_dic["Range"]
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
        # for i in range(len(battery)):
        for i, batr in enumerate(battery):
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
        b.photo = b.photo[0].encode("ascii", "ignore")
        b.save()


class UpdateBike():
    """
    Class used to make sure existing records are updated rather than
    over-written.  This is necessary because comment fields are added by
    the administrator and not found on the propel website.  If records
    were over-written, administrator comments would be lost when the
    scraper was run.
    """

    @staticmethod
    def update_bike(bike_record, b):
        """
        Checks to see if a bike record has had changes to url or price fields.
        If so, it updates these fields.
        Input:  A bike record
        Output: Message indicating function is complete.
        """

        if bike_record.price != b['price']:
            bike_record.price = b['price']
            bike_record.save()
        if bike_record.url != b['url']:
            bike_record.url = b['url']
            bike_record.save()
        return
