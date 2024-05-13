import sqlite3 as sql3


try: 
    db = sql3.connect("Database/arcade-db.sqlite3")
    cursor = db.cursor()
except:
    print("Not Found")