import sqlite3
def init_db(path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''CREATE TABLE admins (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE cakes (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, image TEXT)''')
    c.execute('''CREATE TABLE orders (id INTEGER PRIMARY KEY AUTOINCREMENT, items TEXT, total REAL)''')
    c.execute("INSERT INTO admins (username,password) VALUES ('admin','admin123')")
    c.execute("INSERT INTO cakes (name, price, image) VALUES ('Chocolate Cake', 500.0, '')")
    c.execute("INSERT INTO cakes (name, price, image) VALUES ('Vanilla Cake', 400.0, '')")
    conn.commit()
    conn.close()
