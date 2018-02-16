# -*- coding: utf-8 -*-

import scrapy

# import mysql.connector
# #database connection
# config = {
#     'user': 'root',
#     'password': 'aitpune411015',
#     'host': '127.0.0.1',
#     'database': 'Ali_Final',
#     'raise_on_warnings': True,
#  }

# cnx = mysql.connector.connect(**config)
# cursor = cnx.cursor()
#cnx.close()

from amazon.items import AmazonItem

class AmazonProductSpider(scrapy.Spider):
    #spider name
    name = "amazon"
    #allowed_domains = ["amazon.com"]
    def start_requests(self):
        
        #Use working product URL below
        # start_urls = [
        #   "http://www.amazon.com/dp/B0046UR4F4", "http://www.amazon.com/dp/B00JGTVU5A",
        #   "http://www.amazon.com/dp/B00O9A48N2", "http://www.amazon.com/dp/B00UZKG8QU"
        #  ]   
        
        #AsinList = ['B073XC3Y5J','B07439FYQX','B01EDXQ5QW','B004OWMLZW','B007YX9O9O',]
        
        #url formed as per user defined category
        yield scrapy.Request('http://www.amazon.com/dp/%s' % self.category,callback=self.parse_product_info)
 
    def parse_product_info(self, response):
        
        #Extracting the content using css or xpath selectors
        items = AmazonItem()
        title = response.xpath('//h1[@id="title"]/span/text()').extract()
        sale_price = response.xpath('//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()').extract()
        category = response.xpath('//a[@class="a-link-normal a-color-tertiary"]/text()').extract()
        availability = response.xpath('//div[@id="availability"]//text()').extract()
        
        #create a dictionary to store the scraped info
        items['product_name'] = ''.join(title).strip()
        items['product_sale_price'] = ''.join(sale_price).strip()
        items['product_category'] = ','.join(map(lambda x: x.strip(), category)).strip()
        items['product_availability'] = ''.join(availability).strip()
       
        #yield or give the scraped info [items]        
        yield items