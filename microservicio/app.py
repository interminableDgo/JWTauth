from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import logging

app = Flask(__name__)

# Configuración de la base de datos y JWT
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Trodat74'
app.config['MYSQL_DB'] = 'JWT'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

# Use direct PyMySQL connections (no compiled mysqlclient needed)
jwt = JWTManager(app)
CORS(app)

# Helper to get a DB connection using app.config
def get_connection():
    return pymysql.connect(
        host=app.config.get('MYSQL_HOST', 'localhost'),
        user=app.config.get('MYSQL_USER'),
        password=app.config.get('MYSQL_PASSWORD'),
        database=app.config.get('MYSQL_DB'),
        cursorclass=pymysql.cursors.Cursor,
        autocommit=False,
        charset='utf8mb4'
    )
# Enable CORS so the separate web client can call this API from another origin
CORS(app)

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = generate_password_hash(data.get('password'))

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
    finally:
        conn.close()

    logger.info(f"Usuario registrado: {username}")
    return jsonify({"message": "Usuario registrado exitosamente"}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
    finally:
        conn.close()

    if user and check_password_hash(user[0], password):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        logger.info(f"Usuario autenticado: {username}")
        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
    else:
        logger.warning(f"Intento de login fallido para usuario: {username}")
        return jsonify({"message": "Credenciales inválidas"}), 401

@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    logger.info(f"Token refrescado para usuario: {current_user}")
    return jsonify({"access_token": new_access_token}), 200

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    logger.info(f"Perfil accedido por: {current_user}")
    return jsonify({"username": current_user}), 200

if __name__ == '__main__':
    # Bind to 0.0.0.0 so the service is reachable from other machines on the network
    app.run(host='0.0.0.0', debug=True)