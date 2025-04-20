from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import get_db_connection

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    role = data['role']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if role == "Admin":
        cursor.execute("SELECT * FROM Admin WHERE username=%s AND password=%s", (username, password))
    else:
        cursor.execute("SELECT * FROM Operator WHERE OperatorUser=%s AND OperatorPassword=%s", (username, password))

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success", "role": role})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
