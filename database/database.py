import sqlite3
from datetime import datetime, timedelta
from config import prName, prPrice
from services.calculation import calculatePrice
from services.google_table import STATUS

def get_connection():
    path = "database/database.db"
    return sqlite3.connect(path)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            telegram_id TEXT NOT NULL,
                            date TEXT NOT NULL,
                            name TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            product TEXT NOT NULL,
                            count INTEGER NOT NULL,
                            product_price INTEGER NOT NULL,
                            sum_price INTEGER NOT NULL,
                            status TEXT NOT NULL
                       )
                       ''')
    conn.close()
#add order
def add_order(telegram_id, us):
    date = datetime.now().strftime("%d.%m.%Y")
    sum_pr = calculatePrice(us["product"][prPrice], us["count"])
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO orders (telegram_id, date, name, phone, product, count, product_price, sum_price, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (telegram_id, date, us["name"], us["phone"], us["product"][prName], us["count"], us["product"][prPrice], sum_pr, STATUS))
        orderID = cursor.lastrowid
    conn.close()
    return orderID
#get order_ids
def get_order_ids():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT order_id, status FROM orders WHERE status = (?)''', (STATUS, ))
        rows = cursor.fetchall()
        order_ids = [row[0] for row in rows]
    conn.close()
    return order_ids
#get order with id
def get_order(id):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM orders
                       WHERE order_id = (?)''', (id, ))
        row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None
#change status
def change_status(id, new_status):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE orders SET status = ? WHERE order_id = ?''', (new_status, id))
    cursor.close()
#get last week orders
def get_week_orders():
    now = datetime.now()
    week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d")
    today = now.strftime("%Y-%m-%d")
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM orders WHERE printf("%s-%s-%s", substr(date, 7, 4), substr(date, 4, 2), substr(date, 1, 2)) BETWEEN ? AND ?''', (week_ago, today))
        rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows