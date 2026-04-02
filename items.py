import sqlite3

db = sqlite3.connect('items.db')
cursor = db.cursor()

db.close()