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

#更新顧客對商家或送貨員的評價內容
def update(id, feedback_text, rating, customer_id):
    sql = "UPDATE Feedback SET feedback_text = %s, rating = %s WHERE id = %s AND customer_id = %s;"
    param = (feedback_text, rating, id, customer_id)  
    cursor.execute(sql, param)
    conn.commit() 
    return

#顧客為商家或送貨員提交評價
def addFeedback(customer_id, target_id, feedback_text, rating, created_at):
    sql = "INSERT INTO Feedback (customer_id, target_id, feedback_text, rating, created_at) VALUES (%s, %s, %s, %s, %s);"
    param = (customer_id, target_id, feedback_text, rating, created_at)
    cursor.execute(sql, param)
    conn.commit() 


#查詢某商家的所有評價
def getList(target_id):
    sql = """
    SELECT 
        f.id, 
        f.feedback_text, 
        f.rating, 
        f.created_at, 
        c.name AS customer_name 
    FROM Feedback f
    INNER JOIN Customer c ON f.customer_id = c.id
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
    FROM Feedback f
    INNER JOIN Customer c ON f.customer_id = c.id
    WHERE f.target_id = %s 
      AND f.target_id IN (SELECT id FROM DeliveryPerson);
    """
    cursor.execute(sql, (target_id,))  
    return cursor.fetchall() 
