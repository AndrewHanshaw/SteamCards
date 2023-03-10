import scrapy
from scrapy.crawler import CrawlerProcess
import sqlite3
import urllib.parse
from feeCalc import feeCalc

# Connect to the SQLite database
conn = sqlite3.connect('steamCards.db')
cursor = conn.cursor()

steamIDfromUser = 730 #int(input("Enter Steam ID: "))
cursor.execute('SELECT * FROM cards WHERE steamID=? LIMIT 1', (steamIDfromUser,))
row = cursor.fetchone()
name = row[2]
cardSearchURL = 'https://steamcommunity.com/market/search?q='+urllib.parse.quote_plus('"'+name+' Trading Card"')+'#p1_popular_desc'
boosterSearchURL = 'https://steamcommunity.com/market/search?q='+urllib.parse.quote_plus('"'+name+' Booster Pack"')+'#p1_popular_desc'
results = []

class cardSpider(scrapy.Spider):
    name = "scrapeCards"
    allowed_domains = ["steampowered.com"]
    start_urls = [cardSearchURL]

    def parse(self, response):
        for rowLink in response.css('a.market_listing_row_link'):
            data = {
                'qty': rowLink.css('span.market_listing_num_listings_qty::text').get(),
                'price': rowLink.css('span.normal_price::attr(data-price)').get(),
                'currency': rowLink.css('span.normal_price::attr(data-currency)').get(),
                'normal_price': rowLink.css('span.normal_price span.normal_price::text').get(),
                'url' : rowLink.css('a.market_listing_row_link::attr(href)').get()
            }
            results.append(data)

class boosterSpider(scrapy.Spider):
    name = "scrapeCards"
    allowed_domains = ["steampowered.com"]
    start_urls = [cardSearchURL]

    def parse(self, response):
        for rowLink in response.css('a.market_listing_row_link'):
            data = {
                'qty': rowLink.css('span.market_listing_num_listings_qty::text').get(),
                'price': rowLink.css('span.normal_price::attr(data-price)').get(),
                'currency': rowLink.css('span.normal_price::attr(data-currency)').get(),
                'normal_price': rowLink.css('span.normal_price span.normal_price::text').get(),
                'url' : rowLink.css('a.market_listing_row_link::attr(href)').get()
            }
            results.append(data)

process = CrawlerProcess()
process.crawl(cardSpider)
process.start()
total = 0
for i in results:
    total += int(i['price'])/100
        