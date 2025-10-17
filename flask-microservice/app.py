from flask import Flask, request, jsonify, render_template
from flask_bcrypt import Bcrypt
import pymysql
import jwt
import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Configuration for database and JWT
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'your_database'

# Initialize MySQL connection
connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                             user=app.config['MYSQL_USER'],
                             password=app.config['MYSQL_PASSWORD'],
                             database=app.config['MYSQL_DB'])

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    # Fetch user from database
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    
    if user and bcrypt.check_password_hash(user[0], password):
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    connection.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/books', methods=['GET'])
def get_books():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    return jsonify(books)

@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)