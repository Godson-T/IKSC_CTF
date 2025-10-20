from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from flask_bcrypt import Bcrypt
import os
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_fallback_for_local")
bcrypt = Bcrypt(app)

# DB helper
def get_db():
    conn = sqlite3.connect("ctf.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():  # sourcery skip: last-if-guard
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            conn.commit()
        except sqlite3.IntegrityError as e:
            return f"⚠️ Error: {e}"
        finally:
            conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            # ✅ Store session safely (with default False)
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin']) if 'is_admin' in user.keys() else False

            print("✅ SESSION DATA:", session)  # debug print

            # ✅ Redirect safely
            if session.get('is_admin', False):
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('home'))

        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')


 

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("home.html", user=session.get("username"))

# ---------------- ADMIN DASHBOARD --------------
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    conn = get_db()

    # Total counts
    total_challenges = conn.execute("SELECT COUNT(*) FROM challenges").fetchone()[0]
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_flags_solved = conn.execute("SELECT COUNT(*) FROM solves").fetchone()[0]

    # Solves over time for Chart.js
    solves_over_time = conn.execute("""
        SELECT DATE(created_at) as solve_date, COUNT(*) as count
        FROM solves
        GROUP BY solve_date
        ORDER BY solve_date
    """).fetchall()

    conn.close()

    # Convert to lists for Chart.js
    dates = [row['solve_date'] for row in solves_over_time]
    counts = [row['count'] for row in solves_over_time]

    # Pass everything to template
    return render_template(
        'admin/admin_dashboard.html',
        total_challenges=total_challenges,
        total_users=total_users,
        total_flags_solved=total_flags_solved,
        dates=dates,
        counts=counts
    )

# ---------------- ADMIN CHALLENGES ----------------
@app.route('/admin/challenges')
def admin_challenges():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    conn = get_db()
    all_challenges = conn.execute("SELECT * FROM challenges").fetchall()
    conn.close()
    return render_template('admin/admin_challenges.html', challenges=all_challenges)

# ---------------- ADMIN USERS ----------------
@app.route('/admin/users')
def admin_users():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    conn = get_db()
    all_users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template('admin/admin_users.html', users=all_users)

# ---------------- ADD CHALLENGE ----------------
@app.route('/admin/add-challenge', methods=['GET', 'POST'])
def admin_add_challenge():
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        flag = request.form['flag']
        points = request.form['points']

        conn = get_db()
        conn.execute("INSERT INTO challenges (title, description, flag, points) VALUES (?, ?, ?, ?)",
                     (title, description, flag, points))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_challenges'))

    return render_template('admin/admin_add_challenge.html')

# ---------------- USER CHALLENGES ----------------
@app.route('/challenges')
def challenges():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    all_challenges = [dict(c) for c in conn.execute("SELECT id, title, description, points FROM challenges").fetchall()]
    solved_ids = [row['challenge_id'] for row in conn.execute(
        "SELECT challenge_id FROM solves WHERE user_id=?", (session['user_id'],)).fetchall()]
    conn.close()

    return render_template("challenges.html", challenges=all_challenges, solved_ids=solved_ids)

# ---------------- SUBMIT FLAG ----------------
@app.route('/submit_flag/<int:challenge_id>', methods=['POST'])
def submit_flag(challenge_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    flag = request.form['flag']
    conn = get_db()
    challenge = conn.execute("SELECT * FROM challenges WHERE id=?", (challenge_id,)).fetchone()

    already_solved = conn.execute("SELECT * FROM solves WHERE user_id=? AND challenge_id=?",
                                  (session['user_id'], challenge_id)).fetchone()

    if already_solved:
        conn.close()
        return "⚠️ You already solved this challenge!"

    if challenge and flag == challenge['flag']:
        conn.execute("INSERT INTO solves (user_id, challenge_id) VALUES (?, ?)", (session['user_id'], challenge_id))
        conn.execute("UPDATE users SET score = score + ? WHERE id=?", (challenge['points'], session['user_id']))
        conn.commit()
        conn.close()
        return redirect(url_for('challenges'))
    else:
        conn.close()
        return "❌ Wrong Flag!"

# ---------------- LEADERBOARD ----------------
@app.route('/leaderboard')
def leaderboard():
    conn = get_db()
    leaderboard_data = conn.execute("""
        SELECT username, score, 
               (SELECT COUNT(*) FROM solves WHERE user_id = users.id) AS solved_count
        FROM users
        ORDER BY score DESC
    """).fetchall()
    conn.close()
    return render_template("leaderboard.html", leaderboard=leaderboard_data)

# 1️⃣ Initialize DB and tables
def init_db():
    conn = sqlite3.connect("ctf.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        is_admin INTEGER DEFAULT 0
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        flag TEXT NOT NULL,
        points INTEGER DEFAULT 0
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS solves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        challenge_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

init_db()

if  __name__=="__main__":
    app.run(debug=True)
