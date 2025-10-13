import os
import uvicorn
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from mysql.connector import Error

app = FastAPI()


def get_db_connection():
    """建立資料庫連線；優先使用環境變數設定。"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'testuser'),
        password=os.getenv('DB_PASSWORD', 'testpass'),
        database=os.getenv('DB_NAME', 'testdb'),
        port=int(os.getenv('DB_PORT', '3306')),
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
    except Error as exc:
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
    return 'Service is running on /.'


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8080)
