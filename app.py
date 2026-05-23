# ============================================================
# SMART TASK MANAGEMENT SYSTEM
# Sankar Group — Python Development Internship Assignment
# Candidate: Goudampally Sai Snehitha
# Technologies: Python, Flask, SQLite, REST API, Pandas, WebSockets
# ============================================================

from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_socketio import SocketIO, emit
import sqlite3
import hashlib
import datetime
from analytics import get_analytics

app = Flask(__name__)
app.secret_key = 'sankar_group_internship_2026'
socketio = SocketIO(app, cors_allowed_origins="*")

DB_NAME = 'tasks.db'

# ============================================================
# DATABASE HELPER
# ============================================================
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ============================================================
# AUTHENTICATION ROUTES
# ============================================================

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email    = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            return render_template('register.html', error='All fields are required!')

        db = get_db()
        existing = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            db.close()
            return render_template('register.html', error='Email already registered!')

        db.execute(
            'INSERT INTO users (username, email, password, created_at) VALUES (?, ?, ?, ?)',
            (username, email, hash_password(password), datetime.datetime.now().isoformat())
        )
        db.commit()
        db.close()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')

        db   = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE email = ? AND password = ?',
            (email, hash_password(password))
        ).fetchone()
        db.close()

        if user:
            session['user_id']  = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid email or password!')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ============================================================
# REST API — TASKS
# ============================================================

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    db    = get_db()
    tasks = db.execute(
        'SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()
    db.close()

    return jsonify([dict(t) for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    db = get_db()
    cursor = db.execute(
        '''INSERT INTO tasks (user_id, title, description, priority, status, created_at)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (
            session['user_id'],
            data.get('title'),
            data.get('description', ''),
            data.get('priority', 'Medium'),
            'Pending',
            datetime.datetime.now().isoformat()
        )
    )
    db.commit()
    task_id = cursor.lastrowid
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    db.close()

    # WebSocket — broadcast new task
    socketio.emit('task_added', dict(task))

    return jsonify({'message': 'Task added!', 'task': dict(task)}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    db   = get_db()
    db.execute(
        '''UPDATE tasks SET title=?, description=?, priority=?, status=?
           WHERE id=? AND user_id=?''',
        (
            data.get('title'),
            data.get('description'),
            data.get('priority'),
            data.get('status'),
            task_id,
            session['user_id']
        )
    )
    db.commit()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    db.close()

    # WebSocket — broadcast update
    socketio.emit('task_updated', dict(task))

    return jsonify({'message': 'Task updated!', 'task': dict(task)})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, session['user_id']))
    db.commit()
    db.close()

    # WebSocket — broadcast delete
    socketio.emit('task_deleted', {'id': task_id})

    return jsonify({'message': 'Task deleted!'})

# ============================================================
# ANALYTICS API — Pandas & NumPy
# ============================================================

@app.route('/api/analytics', methods=['GET'])
def analytics():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    result = get_analytics(session['user_id'], DB_NAME)
    return jsonify(result)

# ============================================================
# WEBSOCKET EVENTS
# ============================================================

@socketio.on('connect')
def on_connect():
    emit('connected', {'message': 'Connected to Smart Task Manager!'})

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

# ============================================================
# RUN APP
# ============================================================

if __name__ == '__main__':
    from database import init_db
    init_db()
    print("=" * 50)
    print("  Smart Task Management System")
    print("  Candidate: Goudampally Sai Snehitha")
    print("  Running on http://127.0.0.1:5000")
    print("=" * 50)
    socketio.run(app, debug=True)
