#!/usr/local/bin/python
# Connect to MariaDB Platform
import mysql.connector #mariadb

try:
	#連線DB
	conn = mysql.connector.connect(
		user="root",
		password="",
		host="localhost",
		port=3306,
		database="FoodPangolin"
	)
	#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
	cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
	print(e)
	print("Error connecting to DB")
	exit(1)

def login(name, password):
	sql="SELECT id FROM merchant WHERE name = %s AND password = %s"
	cursor.execute(sql,(name, password))
	record = cursor.fetchone()
	try:
		print(record['id'], " log in...")
		return True, record['id']
	except Exception as e:
		return False, '0'

#新增商家資料
def add_merchant(id, name, location, contact_info):
    sql = "INSERT INTO merchant (id, name, location, contact_info) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (id, name, location, contact_info))
    conn.commit()
    return

#商家為其菜單新增項目
def add_menu_item(id, name, price, description, availability_status, merchant_id):
    sql = "INSERT INTO menuitem (id, name, price, description, availability_status, merchant_id) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql,(id, name, price, description, availability_status, merchant_id))
    conn.commit()
    return

#商家接收到新訂單
def add_order(id, customer_id, merchant_id, delivery_person_id, status, delivery_address, total_price, created_at):
    sql = "INSERT INTO orde (id, customer_id, merchant_id, delivery_person_id, status, delivery_address, total_price, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (id, customer_id, merchant_id, delivery_person_id, status, delivery_address, total_price, created_at))
    conn.commit()
    return

#刪除商家及其相關數據
def delete_merchant(merchant_id):
    sql = "DELETE FROM merchant WHERE id = %s"
    cursor.execute(sql, (merchant_id,))
    conn.commit()
    return

#刪除某商家的菜單項目
def delete_menu_item(menu_item_id):
    sql = "DELETE FROM menuitem WHERE id = %s"
    cursor.execute(sql, (menu_item_id,))
    conn.commit()
    return

#修改商家的基本資料
def update_merchant(name,location,contact_info,id):
    sql = "UPDATE merchant SET name = %s, location = %s, contact_info = %s WHERE id = %s"
    cursor.execute(sql,(name,location,contact_info,id))
    conn.commit()
    return

#更新某商家的菜單項目
def update_menu_item(name, price, description, availability_status, id):
    sql = "UPDATE menuitem SET name = %s, price = %s, description = %s, availability_status = %s WHERE id = %s"
    cursor.execute(sql, (name, price, description, availability_status, id))
    conn.commit()
    return

def get_all_merchant():
    sql = "SELECT id, name FROM merchant"
    cursor.execute(sql)
    products = cursor.fetchall()
    return products

#查詢某商家的詳細資訊
def get_merchant(merchant_id):
    sql = "SELECT id, name, location, contact_info FROM merchant WHERE id = %s"
    cursor.execute(sql, (merchant_id,))
    return cursor.fetchone()

#獲取某商家的所有菜單項目
def get_menu_items(merchant_id):
    sql = "SELECT id, name, price, description, availability_status FROM menuitem WHERE merchant_id = %s"
    cursor.execute(sql, (merchant_id,))
    products = cursor.fetchall()
    print(products)
    return products

#查詢某商家相關的訂單
def get_orders_by_merchant(merchant_id):
    sql = """
    SELECT o.id, o.customer_id, o.status, o.delivery_address, o.total_price, o.created_at 
    FROM orde o
    WHERE o.merchant_id = %s
    """
    cursor.execute(sql, (merchant_id,))
    return cursor.fetchall()

#查詢某商家收到的評價
def get_feedback_by_merchant(merchant_id):
    sql = """
    SELECT f.id, f.customer_id, f.feedback_text, f.rating, f.created_at 
    FROM feedback f
    WHERE f.target_id = %s
    """
    cursor.execute(sql, (merchant_id,))
    return cursor.fetchall()
