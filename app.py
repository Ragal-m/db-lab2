import os
import pymysql
import bcrypt
from datetime import datetime, date
from dotenv import load_dotenv
from functools import wraps
from contextlib import contextmanager
from flask import Flask, render_template, request, redirect, url_for, session, flash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-dev-secret-key')


def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'registration'),
        port=int(os.getenv('DB_PORT', 3306)),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


@contextmanager
def get_cursor():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            yield cursor
    finally:
        conn.close()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('todo_list'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('todo_list'))

    errors = []
    form_data = {'name': '', 'email': ''}

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        form_data['name'] = name
        form_data['email'] = email

        if not name:
            errors.append('Name is required')
        if not email:
            errors.append('Email is required')
        if not password:
            errors.append('Password is required')
        if not confirm_password:
            errors.append('Confirm password is required')
        if password and confirm_password and password != confirm_password:
            errors.append('Passwords do not match')

        if not errors:
            with get_cursor() as cursor:
                cursor.execute("SELECT user_id FROM users WHERE email = %s;", (email,))
                if cursor.fetchone():
                    errors.append('Email Already Exists')
                else:
                    salt = bcrypt.gensalt()
                    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
                    cursor.execute(
                        "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s);",
                        (email, name, hashed_pw)
                    )
                    user_id = cursor.lastrowid
                    session['user_id'] = user_id
                    session['name'] = name
                    return redirect(url_for('todo_list'))

    return render_template('register.html', errors=errors, form_data=form_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('todo_list'))

    errors = []
    form_data = {'email': ''}

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        form_data['email'] = email

        if not email:
            errors.append('Email is required')
        if not password:
            errors.append('Password is required')

        if not errors:
            with get_cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, name, password_hash FROM users WHERE email = %s;",
                    (email,)
                )
                user = cursor.fetchone()

                if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                    session['user_id'] = user['user_id']
                    session['name'] = user['name']
                    return redirect(url_for('todo_list'))
                else:
                    errors.append('Invalid email or password')

    return render_template('login.html', errors=errors, form_data=form_data)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/todos', methods=['GET'])
@login_required
def todo_list():
    now_dt = datetime.now()
    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT todo_id, title, is_done, due_date, created_at 
            FROM todos 
            WHERE user_id = %s 
            ORDER BY is_done ASC, due_date IS NULL ASC, due_date ASC, todo_id DESC;
            """,
            (session['user_id'],)
        )
        todos = cursor.fetchall()

        # Prevent type mismatch errors between date and datetime
        for todo in todos:
            d = todo.get('due_date')
            if d is not None and not isinstance(d, datetime) and isinstance(d, date):
                todo['due_date'] = datetime.combine(d, datetime.min.time())

        # Count total, active, done, and overdue tasks
        cursor.execute(
            """
            SELECT 
                COUNT(*) AS total_count,
                COALESCE(SUM(CASE WHEN is_done = 0 THEN 1 ELSE 0 END), 0) AS active_count,
                COALESCE(SUM(CASE WHEN is_done = 1 THEN 1 ELSE 0 END), 0) AS done_count,
                COALESCE(SUM(CASE WHEN is_done = 0 AND due_date IS NOT NULL AND due_date < %s THEN 1 ELSE 0 END), 0) AS overdue_count
            FROM todos 
            WHERE user_id = %s;
            """,
            (now_dt, session['user_id'])
        )
        counts = cursor.fetchone()
        total_count = int(counts['total_count'] or 0)
        active_count = int(counts['active_count'] or 0)
        done_count = int(counts['done_count'] or 0)
        overdue_count = int(counts['overdue_count'] or 0)

    return render_template(
        'todos.html',
        todos=todos,
        user_name=session.get('name'),
        total_count=total_count,
        active_count=active_count,
        done_count=done_count,
        overdue_count=overdue_count,
        now=now_dt
    )


@app.route('/todos/add', methods=['POST'])
@login_required
def add_todo():
    title = request.form.get('title', '').strip()
    due_date = request.form.get('due_date', '').strip() or None

    if due_date:
        due_date = due_date.replace('T', ' ')

    if not title:
        flash('Title is required', 'error')
    elif len(title) > 200:
        flash('Title is too long', 'error')
    else:
        with get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO todos (user_id, title, due_date) VALUES (%s, %s, %s);",
                (session['user_id'], title, due_date)
            )
    return redirect(url_for('todo_list'))


@app.route('/todos/edit/<int:todo_id>', methods=['POST'])
@login_required
def edit_todo(todo_id):
    title = request.form.get('title', '').strip()
    due_date = request.form.get('due_date', '').strip() or None

    if due_date:
        due_date = due_date.replace('T', ' ')

    if not title:
        flash('Title is required', 'error')
    elif len(title) > 200:
        flash('Title is too long', 'error')
    else:
        with get_cursor() as cursor:
            cursor.execute(
                "UPDATE todos SET title = %s, due_date = %s WHERE todo_id = %s AND user_id = %s;",
                (title, due_date, todo_id, session['user_id'])
            )
    return redirect(url_for('todo_list'))


@app.route('/todos/toggle/<int:todo_id>', methods=['POST'])
@login_required
def toggle_todo(todo_id):
    status = request.form.get('is_done', '0')
    new_status = 1 if status == '1' else 0
    with get_cursor() as cursor:
        cursor.execute(
            "UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s;",
            (new_status, todo_id, session['user_id'])
        )
    return redirect(url_for('todo_list'))


@app.route('/todos/delete/<int:todo_id>', methods=['POST'])
@login_required
def delete_todo(todo_id):
    with get_cursor() as cursor:
        cursor.execute(
            "DELETE FROM todos WHERE todo_id = %s AND user_id = %s;",
            (todo_id, session['user_id'])
        )
    return redirect(url_for('todo_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)