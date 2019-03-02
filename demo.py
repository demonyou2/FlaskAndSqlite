from flask import Flask,request,jsonify
import os,sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

db_file = os.path.join(os.path.dirname(__file__),'demo.db')

@app.route('/userlist', methods=['GET'])
def getAll():
    conn = connectDBbase(db_file)
    cursor = conn.cursor()
    values = cursor.execute('SELECT * FROM USER ORDER BY ID ASC')
    values = values.fetchall()
    return jsonify({'type':'SUCCESS','data':values})

@app.route('/add', methods=['POST'])
def addUser():
    if not request.form.get('id'):
        return 'FAIL'
    id = request.form.get('id')
    name = request.form.get('name')
    score = request.form.get('score')
    conn = connectDBbase(db_file)
    cursor = conn.execute('INSERT INTO USER (ID,NAME,SCORE) VALUES (?,?,?)',(id, name, score))
    closeDBbase(conn,cursor) 
    return 'SUCCESS'

@app.route('/update', methods=['PUT'])
def updateUser():
    if not request.form.get('id'):
        return 'FAIL'
    id = request.form.get('id')
    name = request.form.get('name')
    score = request.form.get('score')
    conn = connectDBbase(db_file)
    cursor=conn.cursor()
    cursor.execute('UPDATE USER SET NAME = ?,SCORE = ? WHERE ID = ?', (name,score,id))
    closeDBbase(conn,cursor)    
    return 'SUCCESS'

@app.route('/delete', methods=['DELETE'])
def deleteUser():
    print(request.form)
    if not request.form.get('id'):
        return 'FAIL'
    id = request.form.get('id')
    conn = connectDBbase(db_file)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM USER WHERE ID = ?', (id,))
    closeDBbase(conn,cursor)
    return 'SUCESS'

def createDBTable(db_file):
    conn = connectDBbase(db_file)
    cursor = conn.cursor()
    value = cursor.execute('''SELECT count(*) FROM sqlite_master WHERE type='table' AND name='USER' ''')
    arr = value.fetchall()
    if arr[0] == (0,):
        cursor.execute('''CREATE TABLE USER
        (ID INT PRIMARY KEY NOT NULL,
        NAME VARCHAR(20) NOT NULL,
        SCORE INT NOT NULL)''')
    closeDBbase(conn,cursor) 

def connectDBbase(db_file):
    return sqlite3.connect(db_file)

def closeDBbase(conn,cursor):
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    createDBTable(db_file)
    app.run()