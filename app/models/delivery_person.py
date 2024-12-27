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
	sql="SELECT id FROM deliveryperson WHERE name = %s AND password = %s"
	cursor.execute(sql,(name, password))
	record = cursor.fetchone()
	try:
		print(record['id'], " log in...")
		return True, record['id']
	except Exception as e:
		return False, '0'

#新增送貨員資料
def add_delivery_person(id, name, vehicle_info, contact_info):
    sql = "INSERT INTO DeliveryPerson (id, name, vehicle_info, contact_info) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql,(id, name, vehicle_info, contact_info))
    conn.commit()
    return

#為送貨員分配訂單
def assign_order_to_delivery(delivery_person_id,order_id):
    sql = "UPDATE Orde SET delivery_person_id = %s, status = 'assigned' WHERE id = %s"
    cursor.execute(sql, (delivery_person_id,order_id))
    conn.commit()
    return

#刪除送貨員資料
def delete_delivery_person(delivery_person_id):
    sql = "DELETE FROM DeliveryPerson WHERE id = %s"
    # param = (delivery_person_id,)
    cursor.execute(sql, (delivery_person_id,))
    conn.commit()
    return

#修改送貨員的基本資料
def update_delivery_person(name,vehicle_info,contact_info,id):
    sql = "UPDATE DeliveryPerson SET name = %s, vehicle_info = %s, contact_info = %s WHERE id = %s"
    cursor.execute(sql, (name,vehicle_info,contact_info,id))
    conn.commit()
    return


#查詢某個送貨員的詳細資料
def get_delivery_person(delivery_person_id):
    sql = "SELECT id, name, vehicle_info, contact_info FROM DeliveryPerson WHERE id = %s"
    # param = (delivery_person_id,)
    cursor.execute(sql, (delivery_person_id,))
    return cursor.fetchone()

#獲取某送貨員的所有分配訂單
def get_orders_by_delivery_person(delivery_person_id):
    sql = """
    SELECT o.id, o.customer_id, o.merchant_id, o.status, o.delivery_address, o.total_price, o.created_at 
    FROM Orde o
    WHERE o.delivery_person_id = %s
    """
    cursor.execute(sql, (delivery_person_id,))
    return cursor.fetchall()

#獲取針對送貨員的評價訊息
def get_feedback_for_delivery_person(delivery_person_id):
    sql = """
    SELECT f.id, f.customer_id, f.feedback_text, f.rating, f.created_at 
    FROM Feedback f
    WHERE f.target_id = %s
    """
    cursor.execute(sql, (delivery_person_id,))
    return cursor.fetchall()
