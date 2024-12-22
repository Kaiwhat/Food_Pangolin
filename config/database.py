import mysql.connector #mariadb

conn = mysql.connector.connect(
    user="root",
    password="",
    host="localhost",
    port=3306,
    database="test"
)
#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
cursor=conn.cursor(dictionary=True)