

import django
django.setup()
import scrapy
import string, csv, json


class PropelSpider(scrapy.Spider):
    name = "propel"
    allowed_domains = ["propelbikes.com"]
    start_urls = [
        "http://propelbikes.com/bikes-by-price/1501-2500",
    ]

    def parse(self, response):
        filename = "input.csv"
        for models in response.xpath('//*[@id="content"]/div[3]/div[3]'):  # goes to grid page of models
            with open(filename, 'wb') as f:
                f.write(string.join(models.xpath('//*[@id="content"]/div[3]/div[3]/div/div[2]/a/text()').extract(), ","))
        csvfile = open('input.csv', 'r')
        jsonfile = open('output.json', 'w')

        fieldnames = ("Model")
        reader = csv.DictReader(csvfile, fieldnames)
        for row in reader:
            json.dump(row, jsonfile)
            jsonfile.write('\n')
