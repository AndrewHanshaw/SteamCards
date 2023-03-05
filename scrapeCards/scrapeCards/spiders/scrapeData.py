import scrapy
from scrapy.crawler import CrawlerProcess
import sqlite3
import urllib.parse



# Connect to the SQLite database
conn = sqlite3.connect('steamCards.db')
cursor = conn.cursor()

steamIDfromUser = int(input("Enter Steam ID: "))
cursor.execute('SELECT * FROM cards WHERE steamID=? LIMIT 1', (steamIDfromUser,))
row = cursor.fetchone()
name = row[2]
cardSearchURL = 'https://steamcommunity.com/market/search?q='+urllib.parse.quote_plus('"'+name+' Trading Card"')+'#p1_popular_desc'
boosterSearchURL = 'https://steamcommunity.com/market/search?q='+urllib.parse.quote_plus('"'+name+' Booster Pack"')+'#p1_popular_desc'

class steamSpider(scrapy.Spider):
    name = "scrapeCards"
    allowed_domains = ["steampowered.com"]
    start_urls = [cardSearchURL]
    settings = crawler.settings 

    def parse(self, response):
        for rowLink in response.css('a.market_listing_row_link'):
            yield {
                'qty': rowLink.css('span.market_listing_num_listings_qty::text').get(),
                'price': rowLink.css('span.normal_price::attr(data-price)').get(),
                'currency': rowLink.css('span.normal_price::attr(data-currency)').get(),
                'normal_price': rowLink.css('span.normal_price span.normal_price::text').get(),
                'url' : rowLink.css('a.market_listing_row_link::attr(href)').get()
            }

class boosterSpider(scrapy.Spider):
    name = "scrapeBooster"
    allowed_domains = ["steampowered.com"]
    start_urls = [boosterSearchURL]

    def parse(self, response):
        for rowLink in response.css('a.market_listing_row_link'):
            yield {
                'qty': rowLink.css('span.market_listing_num_listings_qty::text').get(),
                'price': rowLink.css('span.normal_price::attr(data-price)').get(),
                'currency': rowLink.css('span.normal_price::attr(data-currency)').get(),
                'normal_price': rowLink.css('span.normal_price span.normal_price::text').get(),
                'url' : rowLink.css('a.market_listing_row_link::attr(href)').get()
            }
        

process = CrawlerProcess()
process.crawl(steamSpider)
process.crawl(boosterSpider)
process.start()
a = 1