import csv
import sqlite3
import urllib.parse

conn = sqlite3.connect('steamCards.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE cards (
            id INTEGER PRIMARY KEY,
            steamID INTEGER,
            name TEXT,
            dateAdded DATE,
            cardSearchURL VARCHAR(500),
            boosterSearchURL VARCHAR(500)
    )
''')

with open('csv/STC_set_data_230227.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # skip the header row
    for row in reader:
        name, _, _, _, _, _, _, _, _, _, _, _, _, _, dateAdded, steamID = row
        cardSearchURL = 'https://steamcommunity.com/market/search?q='+urllib.parse.quote_plus('"'+name+' Trading Card"')+'#p1_popular_desc'
        boosterSearchURL = 'https://steamcommunity.com/market/search?q='+urllib.parse.quote_plus('"'+name+' Booster Pack"')+'#p1_popular_desc'
        cursor.execute('INSERT INTO cards (name, steamID, dateAdded, cardSearchURL, boosterSearchURL) VALUES (?, ?, ?, ?, ?)', (name, steamID, dateAdded, cardSearchURL, boosterSearchURL))
        
conn.commit()
conn.close()