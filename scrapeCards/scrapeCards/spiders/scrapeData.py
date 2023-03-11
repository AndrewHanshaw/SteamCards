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
cardSearchURL = 'https://steamcommunity.com/market/search?q='+urllib.parse.quote_plus('"'+name+' Trading Card"')+'#p1_popular_desc'
boosterSearchURL = 'https://steamcommunity.com/market/search?q='+urllib.parse.quote_plus('"'+name+' Booster Pack"')+'#p1_popular_desc'
cards = []
booster = []

class cardSpider(scrapy.Spider):
    name = "scrapeCards"
    allowed_domains = ["steampowered.com"]
    start_urls = [cardSearchURL]

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
expectedSaleValue = expectedSaleValue/len(cards)*3
expectedProfit = expectedSaleValue - booster[0]['price']
print('Expected Profit:', expectedProfit)
        