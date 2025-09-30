import mysql.connector
from flask import Flask

app = Flask(__name__)

@app.route('/products')
def get_products():
    conn = mysql.connector.connect(
        host='localhost',
        user='testuser',
        password='testpass',
        database='testdb',
        port=3306
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Product')
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    # 直接以純文字格式印出
    output = '\t'.join(columns) + '\n'
    for row in results:
        output += '\t'.join(str(item) for item in row) + '\n'
    return f'<pre>{output}</pre>'

@app.route('/good')
def good():
    return 'This is the /good route. Service is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
