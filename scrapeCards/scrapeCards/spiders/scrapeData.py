import scrapy
from scrapy.crawler import CrawlerProcess
import sqlite3
import urllib.parse
import feeCalc

# Connect to the SQLite database
conn = sqlite3.connect('steamCards.db')
cursor = conn.cursor()

steamIDfromUser = int(input("Enter Steam ID: "))
cursor.execute('SELECT * FROM cards WHERE steamID=? LIMIT 1', (steamIDfromUser,))
row = cursor.fetchone()
name = row[2]
cardSearchURL = row[4]
boosterSearchURL = row[5]
cards = []
booster = []

class cardSpider(scrapy.Spider):
    name = "scrapeCards"
    allowed_domains = ["steampowered.com"]
    start_urls = [cardSearchURL]

    custom_settings = {
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
        'LOG_FILE': 'scrapy.log'
    }

    def parse(self, response):
        for rowLink in response.css('a.market_listing_row_link'):
            data = {
                'qty': rowLink.css('span.market_listing_num_listings_qty::text').get(),
                'price': float(rowLink.css('span.normal_price::attr(data-price)').get())/100,
                'currency': int(rowLink.css('span.normal_price::attr(data-currency)').get()),
                'normal_price': rowLink.css('span.normal_price span.normal_price::text').get(),
                'url' : rowLink.css('a.market_listing_row_link::attr(href)').get()
            }
            data['qty'] = int(data['qty'].replace(",",""))
            cards.append(data)

class boosterSpider(scrapy.Spider):
    name = "scrapeBooster"
    allowed_domains = ["steampowered.com"]
    start_urls = [boosterSearchURL]

    custom_settings = {
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
        'LOG_FILE': 'scrapy.log'
    }

    def parse(self, response):
        for rowLink in response.css('a.market_listing_row_link'):
            data = {
                'qty': rowLink.css('span.market_listing_num_listings_qty::text').get(),
                'price': float(rowLink.css('span.normal_price::attr(data-price)').get())/100,
                'currency': int(rowLink.css('span.normal_price::attr(data-currency)').get()),
                'normal_price': rowLink.css('span.normal_price span.normal_price::text').get(),
                'url' : rowLink.css('a.market_listing_row_link::attr(href)').get()
            }
            booster.append(data)

process = CrawlerProcess()
process.crawl(cardSpider)
process.crawl(boosterSpider)
process.start()
expectedSaleValue = 0

for i in cards:
    i['saleValue'] = feeCalc.feeCalc(i['price'])
    expectedSaleValue+=i['saleValue']
expectedSaleValue = round(expectedSaleValue/len(cards)*3,3)
expectedProfit = round(expectedSaleValue - booster[0]['price'], 3)
print('Expected Profit:', expectedProfit)
        