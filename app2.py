import os
import uvicorn
import pymysql
from pymysql.err import MySQLError
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()


def get_db_connection():
    """
    建立資料庫連線；優先使用環境變數設定。
    使用 PyMySQL 連到 MySQL。
    """
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        # 如果你是 docker-compose 對外 3308:3306，就改成預設 3308
        port=int(os.getenv('DB_PORT', '3307')),
        user=os.getenv('DB_USER', 'testuser'),
        password=os.getenv('DB_PASSWORD', 'testpass'),
        database=os.getenv('DB_NAME', 'testdb'),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.Cursor,  # 回傳 tuple，方便下面照你的寫法輸出
    )


@app.get('/products', response_class=HTMLResponse)
def get_products():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Product')
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
    except MySQLError as exc:
        # 資料庫錯誤丟 500
        raise HTTPException(status_code=500, detail=f'Database error: {exc}') from exc
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # 將欄位與資料列格式化為簡單的表格樣式字串。
    lines = ['\t'.join(columns)]
    for row in results:
        lines.append('\t'.join(str(item) for item in row))
    output = '\n'.join(lines)
    return f'<pre>{output}</pre>'


@app.get('/')
def root():
    return 'Service is running on2 /.'


if __name__ == '__main__':
    # 檔名如果是 app.py，就用 "app:app"
    uvicorn.run('app2:app', host='0.0.0.0', port=8090)
