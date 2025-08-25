import os
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import pymysql

# ----- App & Socket.IO -----
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "devsecret")
socketio = SocketIO(app, cors_allowed_origins="*")

# ----- DB Config (from env) -----
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "apppass")

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

def init_db():
    # Safe to call on each start; ensures table exists
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB;
                """
            )

# ----- Health -----
@app.get("/healthz")
def healthz():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return "ok", 200
    except Exception as e:
        return str(e), 500

# ----- REST API -----
@app.get("/api/feedback")
def list_feedback():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, message, created_at FROM feedback ORDER BY id DESC")
            rows = cur.fetchall()
    return jsonify(rows), 200

@app.post("/api/feedback")
def create_feedback():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    message = (data.get("message") or "").strip()
    if not name or not message:
        return {"error": "name and message required"}, 400

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO feedback (name, message) VALUES (%s, %s)", (name, message))
            cur.execute("SELECT id, name, message, created_at FROM feedback ORDER BY id DESC LIMIT 1")
            new_row = cur.fetchone()

    # Broadcast to all connected clients (matches frontend event name)
    socketio.emit("new_feedback", new_row)
    return {"status": "created", "item": new_row}, 201

# ----- Socket events (optional: for connect logging) -----
@socketio.on("connect")
def on_connect():
    # You can log or emit a welcome message if needed
    pass

# ----- Entrypoint (dev) -----
if __name__ == "__main__":
    init_db()
    # Enable debug and use threaded mode to see full errors
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)