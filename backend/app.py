from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Ініціалізація SQLite бази даних
def init_db():
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flowers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/flowers', methods=['GET'])
def get_flowers():
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flowers')
    flowers = cursor.fetchall()
    conn.close()
    return jsonify(flowers)

@app.route('/flowers', methods=['POST'])
def add_flower():
    data = request.json
    conn = sqlite3.connect('flowers.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO flowers (name, price) VALUES (?, ?)', (data['name'], data['price']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Flower added"}), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
