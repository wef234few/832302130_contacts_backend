import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

# 修改数据库路径，适应函数计算环境
if os.path.exists('/mnt/auto'):
    # 在函数计算环境中，使用持久化存储
    DATABASE = '/mnt/auto/contacts.db'
else:
    # 本地开发环境
    DATABASE = 'contacts.db'

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def hello():
    return jsonify({"message": "通讯录后端API运行成功！"})

@app.route('/contacts', methods=['GET'])
def get_contacts():
    """获取所有联系人"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    conn.close()
    
    # 转换为字典列表
    contact_list = []
    for contact in contacts:
        contact_list.append({
            'id': contact[0],
            'name': contact[1],
            'phone': contact[2],
            'email': contact[3],
            'created_time': contact[4]
        })
    
    return jsonify(contact_list)

@app.route('/contacts', methods=['POST'])
def add_contact():
    """添加联系人"""
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email', '')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)',
        (name, phone, email)
    )
    conn.commit()
    contact_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"message": "联系人添加成功", "id": contact_id})

@app.route('/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """修改联系人"""
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email', '')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE contacts SET name=?, phone=?, email=? WHERE id=?',
        (name, phone, email, contact_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({"message": "联系人更新成功"})

@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """删除联系人"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id=?', (contact_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "联系人删除成功"})

# 初始化数据库
init_db()

# 本地开发时运行
if __name__ == '__main__':
    print("数据库初始化完成！")
    print("API服务运行在: http://127.0.0.1:5000")
    app.run(debug=True)
