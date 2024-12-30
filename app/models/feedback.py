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

#更新顧客對商家或送貨員的評價內容
def update(id, feedback_text, rating, customer_id):
    sql = "UPDATE feedback SET feedback_text = %s, rating = %s WHERE id = %s AND customer_id = %s;"
    param = (feedback_text, rating, id, customer_id)  
    cursor.execute(sql, param)
    conn.commit() 
    return

#顧客為商家或送貨員提交評價
def addFeedback(order_id, customer_id, feedback_text, rating_m, rating_d, deliveryperson_id, merchant_id):
    sql = "INSERT INTO feedback (order_id, customer_id, feedback_text, rating_m, rating_d, created_at, deliveryperson_id, merchant_id) VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s);"
    param = (order_id, customer_id, feedback_text, rating_m, rating_d, deliveryperson_id, merchant_id)
    cursor.execute(sql, param)
    conn.commit() 

def viewFeedback(order_id):
    sql = """
SELECT 
    o.id AS order_id,
    o.customer_id,
    o.merchant_id,
    o.delivery_person_id,
    o.status,
    o.delivery_address,
    o.total_price,
    o.created_at,
    oi.menu_item_id,
    mi.name AS menu_item_name,  -- 加入 menuitem 的 name
    oi.quantity,
    oi.price AS item_price,
    (oi.quantity * oi.price) AS total_price_per_item
FROM 
    orde o
JOIN 
    orderitem oi ON o.id = oi.order_id
JOIN 
    menuitem mi ON oi.menu_item_id = mi.id  -- 關聯到 menuitem 表
WHERE
    o.id = %s
ORDER BY 
    o.id;
    """
    cursor.execute(sql, (order_id,))
    result = cursor.fetchall()  # 獲取查詢結果
    return result

#查詢某商家的所有評價
def getList(target_id):
    sql = """
    SELECT 
        f.id, 
        f.feedback_text, 
        f.rating, 
        f.created_at, 
        c.name AS customer_name 
    FROM feedback f
    INNER JOIN customer c ON f.customer_id = c.id
    WHERE f.target_id = %s 
      AND f.target_id IN (SELECT id FROM Merchant);
    """
    cursor.execute(sql, (target_id,))  
    return cursor.fetchall()  

#查詢某送貨員的所有評價
def getList(target_id):
    sql = """
    SELECT 
        f.id, 
        f.feedback_text, 
        f.rating, 
        f.created_at, 
        c.name AS customer_name 
    FROM feedback f
    INNER JOIN customer c ON f.customer_id = c.id
    WHERE f.target_id = %s 
      AND f.target_id IN (SELECT id FROM DeliveryPerson);
    """
    cursor.execute(sql, (target_id,))  
    return cursor.fetchall() 
