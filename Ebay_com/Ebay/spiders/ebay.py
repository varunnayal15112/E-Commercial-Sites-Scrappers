# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 13:48:05 2017

@author: vicky
"""

# -*- coding: utf-8 -*-
import scrapy

import mysql.connector
#database connection
config = {
    'user': 'root',
    'password': 'aitpune411015',
    'host': '127.0.0.1',
    'database': 'Ali_Final',
    'raise_on_warnings': True,
 }

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
#cnx.close()

class EbayProductSpider(scrapy.Spider):
    #spider name
    name = 'ebay'
    
    def start_requests(self):
        #url formed as per user defined category
        #_dmd=2 for grid view
        yield scrapy.Request('https://www.ebay.com/sch/i.html?rt=nc&_dmd=2&_nkw=%s' % self.category,callback=self.parse)
        
    def parse(self,response):
        #Extracting the content using css selectors
        start_urls=[]
        for i in range(0,5):
            link=str(response.css("div.gvtitle a.vip::attr(href)")[i].extract())
            start_urls.append(link)
        for url in start_urls:
            print(url)
            #calling parse function as per url to scrap info related to the product link
            yield scrapy.Request(url=url, callback=self.parse_product_info)
        info={
            'hello':'varun',
          }
        yield info
        
    def parse_product_info(self, response):
        
        #Extracting the content using css or xpath selectors
        url=str(response.xpath('/html/head/link[13]/@href').extract_first())
        #currency=str(response.xpath('.//*[@class="p-symbol"]/text()').extract_first())
        price=str(response.xpath('//*[@id="prcIsum"]/text()').extract_first())
        if price=='':
            price=str(response.xpath('//*[@id="mm-saleOrgPrc"]/text()').extract_first())
            discount_price=str(response.xpath('//*[@id="mm-saleDscPrc"]/text()').extract_first())
        else:
            discount_price='none'
        #if price==' - ':
        #    price=str(response.xpath('.//*[@class="p-price"]/span/text()').extract_first())+"-"+str(response.xpath('.//*[@class="p-price"]/span[2]/text()').extract_first())
        #price=currency+price
        #discount_price=str(response.xpath('//*[@id="j-sku-discount-price"]/text()').extract_first())
        title=str(response.xpath('//*[@id="itemTitle"]/text()').extract_first())
        product_rating=str(response.xpath('//*[@id="histogramid"]/div/div[1]/span[1]/text()').extract_first())
        if product_rating=='':
            product_rating='none'
        else:
            product_rating=product_rating[3:]
        product_rating_count=str(response.xpath('//*[@id="_rvwlnk"]/text()').extract_first())  
               
        #item_specifics=str(response.css(".ui-box.product-property-main span::text").extract())
        item_specifics='none'
        seller_name=str(response.xpath('//*[@id="mbgLink"]/span/text()').extract_first())
        shipping_cost=str(response.xpath('.//*[@id="fshippingCost"]//span/text()').extract_first())
        if shipping_cost=='':
            shipping_cost='none'
        seller_rating=str(response.xpath('.//*[@id="si-fb"]/text()').extract_first())
        
        print ('URL :',url)
        #print('CURRENCY :',currency)
        print ('Price :',price)
        print ('D_Price :',discount_price)
        print ('Title :',title)
        print ('P_Rating :',product_rating)
        print ('P_R_Count :',product_rating_count)
        print ('Item_Specifics :',item_specifics)
        print ('Seller_Name :',seller_name)
        print ('Shipping_Cost :',shipping_cost)    
        print ('Seller_Rating :',seller_rating)
        
         
        cursor.execute("""INSERT INTO AliExpress VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""" , (url,price,discount_price,title,product_rating,product_rating_count,item_specifics,seller_name))
        print ("%d rows were inserted" % cursor.rowcount)        
        cnx.commit()
        
        #create a dictionary to store the scraped info
        scraped_info = {

            'url' : url,
            'price' : price,
            'discount_price' : discount_price,
            'title' : title,
            'product_rating' : product_rating,
            'product_rating_count' : product_rating_count,
            'item_specifics' : item_specifics,
            'seller_name' : seller_name,
            'shipping_cost' : shipping_cost, 
            'seller_rating' : seller_rating,
        }
            
        #yield or give the scraped info to scrapy
        yield scraped_info

