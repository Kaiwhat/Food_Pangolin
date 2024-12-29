#!/usr/local/bin/python
# Connect to MariaDB Platform
import mysql.connector  # 使用 MariaDB

try:
    # 連線至資料庫
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="FoodPangolin"  # 確保名稱正確
    )
    cursor = conn.cursor(dictionary=True)  # 建立 cursor，返回 dictionary 格式的結果
except mysql.connector.Error as e:
    print(e)
    print("Error connecting to DB")
    exit(1)

# 新增商品到購物車
def add_to_cart(customer_id, menuitem_id, quantity):
    """
    將商品加入購物車
    """
    sql = "INSERT INTO cart (customer_id, menuitem_id, quantity) VALUES (%s, %s, %s) " \
          "ON DUPLICATE KEY UPDATE quantity = quantity + %s;"
    cursor.execute(sql, (customer_id, menuitem_id, quantity, quantity))
    conn.commit()
    print(f"menuitem {menuitem_id} added to cart for customer {customer_id}.")

# 從購物車移除商品
def remove_from_cart(customer_id, menuitem_id):
    """
    從購物車移除指定商品
    """
    sql = "DELETE FROM cart WHERE customer_id = %s AND menuitem_id = %s;"
    cursor.execute(sql, (customer_id, menuitem_id))
    conn.commit()
    print(f"menuitem {menuitem_id} removed from cart for customer {customer_id}.")

# 檢視購物車內容
def view_cart(customer_id):
    """
    查看顧客的購物車內容
    """
    sql = "SELECT c.menuitem_id, p.name AS menuitem_name, c.quantity, p.price, (c.quantity * p.price) AS total_price, m.name AS merchant_name  " \
          "FROM cart c " \
          "JOIN menuitem p ON c.menuitem_id = p.id " \
          "JOIN merchant m ON p.merchant_id = m.id " \
          "WHERE c.customer_id = %s;"
    cursor.execute(sql, (customer_id,))
    results = cursor.fetchall()
    print(f"Cart for customer {customer_id}: {results}")
    return results

# 清空購物車
def clear_cart(customer_id):
    """
    清空顧客的購物車
    """
    sql = "DELETE FROM cart WHERE customer_id = %s;"
    cursor.execute(sql, (customer_id,))
    conn.commit()
    print(f"Cart cleared for customer {customer_id}.")

# 結帳並轉換為訂單
def checkout(customer_id, order_id, delivery_address):
    """
    結帳，將購物車內容轉為訂單
    """
    # 確認購物車內容
    cart_items = view_cart(customer_id)
    if not cart_items:
        print("Cart is empty. Cannot proceed to checkout.")
        return

    # 插入訂單
    sql_order = "INSERT INTO orders (id, customer_id, delivery_address, status, total_price) VALUES (%s, %s, %s, %s, %s);"
    total_price = sum(item['total_price'] for item in cart_items)
    cursor.execute(sql_order, (order_id, customer_id, delivery_address, 'Pending', total_price))
    
    # 插入訂單項目
    sql_order_items = "INSERT INTO order_items (order_id, menuitem_id, quantity, price) VALUES (%s, %s, %s, %s);"
    for item in cart_items:
        cursor.execute(sql_order_items, (order_id, item['menuitem_id'], item['quantity'], item['total_price']))

    # 清空購物車
    clear_cart(customer_id)

    conn.commit()
    print(f"Order {order_id} placed for customer {customer_id}. Total price: {total_price}.")
