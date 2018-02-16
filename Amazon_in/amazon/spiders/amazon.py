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
    #allowed_domains = ["amazon.in"]
    def start_requests(self):
        
        #AsinList = ['B01H5EBBX8','B0751LYPY3','B002U1ZBG0','B01HQ4NZE0','B01DU10H2G',]
        
        #url formed as per user defined category
        yield scrapy.Request('http://www.amazon.in/dp/%s' % self.category,callback=self.parse_product_info)
 
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
