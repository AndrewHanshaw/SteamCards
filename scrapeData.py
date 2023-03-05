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
storeSearchUrl = 'https://steamcommunity.com/market/search?q='+urllib.parse.quote_plus('"'+name+' Trading Card"')

class steamSpider(scrapy.Spider):
    name = "scrapeCards"
    allowed_domains = ["steampowered.com"]
    start_urls = [storeSearchUrl]

    def parse(self, response):
        for rowLink in response.css('a.market_listing_row_link'):
            yield {
                'qty': rowLink.css('span.market_listing_num_listings_qty::text').get(),
                'price': rowLink.css('span.normal_price::attr(data-price)').get(),
                'currency': rowLink.css('span.normal_price::attr(data-currency)').get(),
            }

process = CrawlerProcess()
process.crawl(steamSpider)
process.start()