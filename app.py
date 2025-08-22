import mysql.connector

def query_mysql():
    # 建立連線
    conn = mysql.connector.connect(
        host='localhost',
        user='testuser',
        password='testpass',
        database='testdb'
    )
    cursor = conn.cursor()

    # 執行查詢
    cursor.execute('SELECT * FROM Product')
    results = cursor.fetchall()

    # 輸出結果
    for row in results:
        print(row)

    # 關閉連線
    cursor.close()
    conn.close()

if __name__ == '__main__':
    query_mysql()