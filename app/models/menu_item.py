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

#將菜單項目添加到訂單
def add_menu_item_to_order(order_id, menu_item_id, quantity, price):
    sql = "INSERT INTO OrderItem (order_id, menu_item_id, quantity, price) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (order_id, menu_item_id, quantity, price))
    conn.commit()
    return

#刪除菜單項目
def delete_menu_item(menu_item_id):
    sql = "DELETE FROM MenuItem WHERE id = %s"
    cursor.execute(sql, (menu_item_id,))
    conn.commit()
    return

# 更新菜單項目資料
def update_menu_item(name, price, description, availability_status, id):
    sql = "UPDATE MenuItem SET name = %s, price = %s, description = %s, availability_status = %s WHERE id = %s"
    cursor.execute(sql, (name, price, description, availability_status, id))
    conn.commit()
    return

# 更新菜單項目的可用狀態
def update_menu_item_availability(availability_status, id):
    sql = "UPDATE MenuItem SET availability_status = %s WHERE id = %s"
    cursor.execute(sql,(availability_status, id))
    conn.commit()
    return


# 查詢菜單項目資料
def get_menu_item(menu_item_id):
    sql = "SELECT id, name, price, description, availability_status, merchant_id FROM MenuItem WHERE id = %s"
    cursor.execute(sql, (menu_item_id))
    return cursor.fetchone()

# 查詢商家的所有菜單項目
def get_menu_items_by_merchant(merchant_id):
    sql = "SELECT id, name, price, description, availability_status FROM menuitem WHERE merchant_id = %s"
    cursor.execute(sql, (merchant_id,))
    products = cursor.fetchall()
    return products

# 查詢訂單中的所有菜單項目
def get_order_items(order_id):
    sql = """
    SELECT oi.id, oi.menu_item_id, mi.name, oi.quantity, oi.price 
    FROM OrderItem oi
    INNER JOIN MenuItem mi ON oi.menu_item_id = mi.id
    WHERE oi.order_id = %s
    """
    cursor.execute(sql, (order_id,))
    return cursor.fetchall()

