import scrapy
import csv
import sqlite3

conn = sqlite3.connect('steamCards.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE cards (
            id PRIMARY KEY,
            steamID INTEGER,
            name TEXT,
            dateAdded DATE
    )
''')

with open('csv/STC_set_data_230227.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # skip the header row
    for row in reader:
        name, _, _, _, _, _, _, _, _, _, _, _, _, _, dateAdded, steamID = row
        cursor.execute('INSERT INTO cards (name, steamID, dateAdded) VALUES (?, ?, ?)', (name, steamID, dateAdded))
conn.commit()
conn.close()