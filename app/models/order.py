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

#新增訂單
def add_order(id, customer_id, delivery_person_id, status, delivery_address, total_price, created_at):
    sql = """
    INSERT INTO orde (id, customer_id, delivery_person_id, status, delivery_address, total_price, created_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    conn.commit()
    sql = """
    SELECT id FROM orde ORDER BY id DESC LIMIT 1;
    """
    cursor.execute(sql,)
    return

def add_order_item(order_id, menu_item_id, quantity, price):
    sql = "INSERT INTO orderitem (order_id, menu_item_id, quantity, price) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (order_id, menu_item_id, quantity, price))
    conn.commit()
    return

#刪除訂單
def delete_order(order_id):
    sql = "DELETE FROM orde WHERE id = %s AND status IN ('pending', 'cancelled')"
    cursor.execute(sql, (order_id,))
    conn.commit()
    return

#更新訂單狀態
def update_order_status(status,id):
    sql = "UPDATE orde SET status = %s WHERE id = %s"
    cursor.execute(sql, (status,id))
    conn.commit()
    return

# 查詢訂單詳細資料
def get_order(order_id):
    sql = """
    SELECT id, customer_id, merchant_id, delivery_person_id, status, delivery_address, total_price, created_at
    FROM orde
    WHERE id = %s
    """
    cursor.execute(sql, (order_id,))
    return cursor.fetchone()

#查詢顧客的所有訂單
def get_orders_by_customer(customer_id):
    sql = """
    SELECT id, merchant_id, delivery_person_id, status, delivery_address, total_price, created_at
    FROM orde
    WHERE customer_id = %s
    """
    cursor.execute(sql, (customer_id,))
    return cursor.fetchall()

#查詢商家的所有訂單
def get_orders_by_merchant(merchant_id):
    sql = """
    SELECT id, customer_id, delivery_person_id, status, delivery_address, total_price, created_at
    FROM orde
    WHERE merchant_id = %s
    """
    cursor.execute(sql, (merchant_id,))
    return cursor.fetchall()

# 查詢送貨員負責的所有訂單
def get_orders_by_delivery_person(delivery_person_id):
    sql = """
    SELECT id, customer_id, merchant_id, status, delivery_address, total_price, created_at
    FROM orde
    WHERE delivery_person_id = %s
    """
    cursor.execute(sql, (delivery_person_id,))
    return cursor.fetchall()

# 查詢訂單中的所有菜單項目
def get_order_items(order_id):
    sql = """
    SELECT oi.id, oi.menu_item_id, mi.name, oi.quantity, oi.price
    FROM orderitem oi
    INNER JOIN menuitem mi ON oi.menu_item_id = mi.id
    WHERE oi.order_id = %s
    """
    cursor.execute(sql, (order_id,))
    return cursor.fetchall()

#插入 OrderItem 資料（假設 Order 資料已經插入，並取得訂單 ID）
def add(order_id, menu_item_id, quantity, price):
	sql="insert into orderitem (order_id, menu_item_id, quantity, price) values (%s, %s, %s, %s);"
	#param=('值',...)
	cursor.execute(sql, (order_id, menu_item_id, quantity, price))
	conn.commit()
	return

# Delete：顧客取消訂單時，刪除訂單資料及訂單項目
def delete(order_id):
	sql="delete from orderitem where order_id = %s;"
	cursor.execute(sql,(order_id,))
	conn.commit()
	return

#查詢顧客所有訂單
def getList(customer_id):
	sql="select id, status, delivery_address, total_price, created_at from orde where customer_id = %s;"
	cursor.execute(sql,(customer_id))
	return cursor.fetchall()





