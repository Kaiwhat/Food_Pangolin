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
def add_order(customer_id, merchant_id, status, delivery_address, total_price):
    """
    插入一筆訂單資料，並返回新插入的訂單 ID。
    """
    try:
        # 插入訂單
        sql_insert = """
        INSERT INTO orde (customer_id, merchant_id, status, delivery_address, total_price, created_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(sql_insert, (customer_id, merchant_id, status, delivery_address, total_price))

        # 提交事務
        conn.commit()
        sql = """
        SELECT id FROM orde ORDER BY id DESC LIMIT 1;
        """
        cursor.execute(sql,)
        record = cursor.fetchone()
        return record['id']
    except Exception as e:
        # 發生錯誤時回滾事務
        conn.rollback()
        print("Error inserting order:", e)
        return None


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
def update_order_status(id):
    sql = "UPDATE orde SET status = '已送達' WHERE id = %s"
    cursor.execute(sql, (id,))
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
SELECT 
    o.id AS order_id,
    o.merchant_id,
    o.delivery_person_id,
    o.status,
    o.delivery_address,
    o.total_price,
    o.created_at,
    f.rating_m AS merchant_rating,
    f.rating_d AS delivery_rating
FROM 
    orde o
LEFT JOIN 
    feedback f ON o.id = f.order_id
WHERE 
    o.customer_id = %s;
    """
    cursor.execute(sql, (customer_id,))
    return cursor.fetchall()

#查詢商家的所有訂單
def get_orders_by_merchant(merchant_id):
    sql = """
SELECT 
    o.id AS order_id,
    o.customer_id,
    o.delivery_address,
    o.total_price,
    oi.menu_item_id,
    mi.name AS menu_item_name,
    oi.quantity,
    oi.price AS item_price,
    (oi.quantity * oi.price) AS item_total_price
FROM 
    orde o
JOIN 
    orderitem oi ON o.id = oi.order_id
JOIN 
    menuitem mi ON oi.menu_item_id = mi.id
WHERE 
    mi.merchant_id = %s 
ORDER BY 
    o.id;
    """
    cursor.execute(sql, (merchant_id,))
    return cursor.fetchall()

# 查詢送貨員負責的歷史訂單
def get_orders_by_delivery_person(delivery_person_id):
    sql = """
    SELECT 
    orde.id, 
    customer.name AS customer_name, 
    merchant.name AS merchant_name, 
    feedback.rating AS delivery_rating, 
    orde.created_at, 
    orde.delivery_address, 
    orde.total_price, 
    orde.pay, 
    deliveryperson.total_pay,  
    orde.created_at
    FROM 
        orde
    JOIN 
        merchant ON orde.merchant_id = merchant.id
    JOIN 
        customer ON orde.customer_id = customer.id
    LEFT JOIN 
        feedback ON orde.delivery_person_id = feedback.deliveryperson_id
    JOIN 
        deliveryperson ON orde.delivery_person_id = deliveryperson.id  
    WHERE 
        orde.delivery_person_id = %s AND orde.status = '已送達';

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


def All_pending_orders():
    sql = """
    SELECT orde.id, orde.customer_id, customer.name AS customer_name, orde.delivery_address, 
           orde.total_price,orde.pay, orde.status, merchant.name AS merchant_name, merchant.location AS merchant_location
    FROM orde
    JOIN merchant ON orde.merchant_id = merchant.id
    JOIN customer ON orde.customer_id = customer.id
    WHERE orde.status = '等待配送';
    """
    cursor.execute(sql)
    return cursor.fetchall()

#配送員接單後將訂單delivery_person_id改變狀態改為"正在配送"
def delivery_add_order(delivery_person_id,id):
    sql = "UPDATE orde SET status = '正在配送',delivery_person_id= %s WHERE id = %s"
    cursor.execute(sql, (delivery_person_id,id,))
    conn.commit()
    return

#總傭金
def add_total_pay(delivery_person_id,id):
    sql="""
    UPDATE deliveryperson
    SET total_pay = total_pay + (
        SELECT pay 
        FROM orde 
        WHERE delivery_person_id = %s AND id = %s
    )
    WHERE id = %s;
    """
    cursor.execute(sql, (delivery_person_id,id,delivery_person_id))
    conn.commit()
    return
     

#獲取某送貨員的所有分配訂單
def get_orders_by_delivery(delivery_person_id):
    sql = """
    SELECT orde.id, orde.customer_id, customer.name AS customer_name, orde.delivery_address, 
           orde.total_price, orde.status, merchant.name AS merchant_name, merchant.location AS merchant_location
    FROM orde 
    JOIN merchant ON orde.merchant_id = merchant.id
    JOIN customer ON orde.customer_id = customer.id
    WHERE orde.delivery_person_id = %s AND orde.status = '正在配送';
    """
    cursor.execute(sql, (delivery_person_id,))
    return cursor.fetchall()




