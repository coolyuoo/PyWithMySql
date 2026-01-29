import os
import pymysql
from pymysql.err import MySQLError
from flask import Flask, abort

app = Flask(__name__)


def get_db_connection():
    """
    建立資料庫連線；優先使用環境變數設定。
    使用 PyMySQL 連到 MySQL。
    """
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'mysql-container'),
        # 如果你是 docker-compose 對外 3308:3306，就改成預設 3308
        port=int(os.getenv('DB_PORT', '3306')),
        user=os.getenv('DB_USER', 'testuser'),
        password=os.getenv('DB_PASSWORD', 'testpass'),
        database=os.getenv('DB_NAME', 'testdb'),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.Cursor,  # 回傳 tuple
    )


@app.route('/products', methods=['GET'])
def get_products():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Product')
        results = cursor.fetchall()

        # 取得欄位名稱
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
        else:
            columns = []

        # 將欄位與資料列格式化為簡單的表格樣式字串
        lines = ['\t'.join(columns)]
        for row in results:
            lines.append('\t'.join(str(item) for item in row))
        output = '\n'.join(lines)

        # Flask 直接回傳字串即可，瀏覽器會將其視為 HTML
        return f'<pre>{output}</pre>'

    except MySQLError as exc:
        # 資料庫錯誤，回傳 500 狀態碼與錯誤訊息
        return f'Database error: {exc}', 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/', methods=['GET'])
def root():
    return 'hello taiwandocker'


if __name__ == '__main__':
    # Flask 內建開發伺服器啟動方式
    # debug=True 方便開發時除錯，正式環境建議關閉
    app.run(host='0.0.0.0', port=8090, debug=True)