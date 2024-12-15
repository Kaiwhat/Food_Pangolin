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
		database="test"
	)
	#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
	cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
	print(e)
	print("Error connecting to DB")
	exit(1)

    # 將菜單項目添加到訂單
def add_order_item(order_id, menu_item_id, quantity, price):
    sql = "INSERT INTO OrderItem (order_id, menu_item_id, quantity, price) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (order_id, menu_item_id, quantity, price))
    conn.commit()
    return

# 刪除訂單中的菜單項目
def delete_order_item(order_item_id):
    sql = "DELETE FROM OrderItem WHERE id = %s"
    cursor.execute(sql, (order_item_id,))
    conn.commit()
    return

# 更新訂單項目的數量或價格
def update_order_item(quantity,price,order_item_id):
    sql = "UPDATE OrderItem SET quantity = %s, price = %s WHERE id = %s"
    cursor.execute(sql, (quantity,price,order_item_id))
    conn.commit()
    return

# 更新訂單項目的價格
def update_order_item_price(price,order_item_id):
    sql = "UPDATE OrderItem SET price = %s WHERE id = %s"
    cursor.execute(sql, (price,order_item_id))
    conn.commit()
    return

# 查詢訂單項目的詳細資料
def get_order_item(order_item_id):
    sql = """
    SELECT id, order_id, menu_item_id, quantity, price
    FROM OrderItem
    WHERE id = %s
    """
    cursor.execute(sql, (order_item_id,))
    return cursor.fetchone()

# 查詢訂單中的所有菜單項目
def get_order_items_by_order(order_id):
    sql = """
    SELECT oi.id, oi.menu_item_id, mi.name, oi.quantity, oi.price
    FROM OrderItem oi
    INNER JOIN MenuItem mi ON oi.menu_item_id = mi.id
    WHERE oi.order_id = %s
    """
    cursor.execute(sql, (order_id,))
    return cursor.fetchall()
