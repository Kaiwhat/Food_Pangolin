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

def connect_db():
    return mysql.connector.connect(
        user="root",
        password="",
        host="localhost",  # 或 "127.0.0.1"
        port=3306,
        database="FoodPangolin"  # 確保這裡是你的資料庫名稱
    )

#顧客登入
def login(name, password):
	sql="SELECT id FROM customer WHERE name = %s AND password = %s"
	cursor.execute(sql,(name, password))
	record = cursor.fetchone()
	try:
		print(record['id'], " log in...")
		return True, record['id']
	except Exception as e:
		return False, '0'

#新增顧客
def add_customer(id, name, contact_info, address, password):
	sql="insert into customer (id, name, contact_info, address, password) values (%s, %s, %s, %s, %s);"
	cursor.execute(sql,(id, name, contact_info, address, password))
	conn.commit()
	return
#刪除顧客
def delete_customer(id):
	sql="delete from customer where id = %s;"
	cursor.execute(sql,(id,))
	conn.commit()
	return


#更新顧客的資訊
def update(id, name, contact_info, address):
	sql="update customer set name = %s, contact_info = %s, address = %s where id = %s;"
	cursor.execute(sql,(name, contact_info, address, id))
	conn.commit()
	return

#查詢顧客的基本資料
def getList(id):
	sql="select name, contact_info, address from customer where id = %s;"
	cursor.execute(sql,)
	return cursor.fetchall()

#當顧客下單時，插入訂單及訂單項目資料
def add(id, customer_id, merchant_id, delivery_person_id, status, delivery_address, total_price, created_at):
	sql="insert into orde (id, customer_id, merchant_id, delivery_person_id, status, delivery_address, total_price, created_at) values (%s, %s, %s, %s, %s, %s, %s, %s);"
	cursor.execute(sql,(id, customer_id, merchant_id, delivery_person_id, status, delivery_address, total_price, created_at))
	conn.commit()
	return


#刪除 Order 資料
def delete(id):
	sql="delete from orde where id = %s;"
	cursor.execute(sql,(id,))
	conn.commit()
	return

#更新 Order 資料（例如顧客修改訂單的送貨地址）
def update(customer_id, delivery_address, status, order_id):
	sql="update orde set delivery_address = %s, status = %s where id = %s and customer_id = %s;"
	cursor.execute(sql,(delivery_address, status, order_id, customer_id))
	conn.commit()
	return

#查詢顧客對商家或送貨員的評價：
def getList(customer_id):
	sql="select f.id, f.feedback_text, f.rating, f.created_at, m.name as merchant_name, d.name as delivery_person_name from feedback f left join merchant m on f.target_id = m.id left join deliveryperson d on f.target_id = d.id where f.customer_id = %s;"
	cursor.execute(sql,(customer_id))
	return cursor.fetchall()

#插入 Feedback 資料（顧客提交對商家或送貨員的評價）
def add(customer_id, target_id, feedback_text, rating, created_at):
    sql = "INSERT INTO feedback (customer_id, target_id, feedback_text, rating, created_at) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(sql, (customer_id, target_id, feedback_text, rating, created_at))  # 傳遞所有需要的參數
    conn.commit()




