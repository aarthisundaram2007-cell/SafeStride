from pathlib import Path
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
from supabase import create_client
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import base64
import io
from datetime import datetime
import requests
import qrcode


class SupabaseUnavailableError(RuntimeError):
    """Raised when Supabase is unavailable or the project is paused."""


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise RuntimeError(f"SUPABASE_URL was not loaded from {ENV_FILE}")

url_loaded = bool(SUPABASE_URL)
key_loaded = bool(SUPABASE_KEY)
url_hostname = urlparse(SUPABASE_URL).hostname if SUPABASE_URL else "unknown"

print(
    f"Supabase diagnostics: URL loaded={url_loaded}, key loaded={key_loaded}, hostname={url_hostname}"
)

supabase = None
if SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as exc:
        print(f"Supabase client initialization failed: {exc}")
        supabase = None
else:
    print("Supabase key not found; Supabase features will be disabled until the key is available.")


def get_supabase_client():
    if supabase is None:
        raise SupabaseUnavailableError("Supabase client is unavailable right now.")
    return supabase

app = Flask(__name__)
app.secret_key = "safestride-secret-key"

DB_PATH = BASE_DIR / "database.db"


def get_db():
    os.makedirs(BASE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(BASE_DIR, exist_ok=True)
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                streak INTEGER DEFAULT 0,
                preparedness_level TEXT DEFAULT 'Beginner',
                profile_photo TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS emergency_contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                relation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS sos_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                latitude REAL,
                longitude REAL,
                message TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                icon TEXT,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id, title)
            );

            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                xp_earned INTEGER DEFAULT 0,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS checklist_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                phone_charged INTEGER DEFAULT 0,
                contacts_added INTEGER DEFAULT 0,
                live_sharing INTEGER DEFAULT 0,
                sos_tested INTEGER DEFAULT 0,
                route_checked INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id)
            );

            CREATE TABLE IF NOT EXISTS stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT,
                lesson TEXT,
                body TEXT,
                image TEXT
            );

            CREATE TABLE IF NOT EXISTS emergency_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT,
                latitude REAL,
                longitude REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS emergency_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                contact_name TEXT,
                contact_phone TEXT,
                relation TEXT,
                method TEXT,
                status TEXT,
                time_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                alert_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS live_sharing_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                latitude REAL,
                longitude REAL,
                method TEXT,
                recipients TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS location_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                path TEXT,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS safety_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                weekly_progress INTEGER DEFAULT 0,
                monthly_progress INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id)
            );

            CREATE TABLE IF NOT EXISTS daily_challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                xp_earned INTEGER DEFAULT 0,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS learning_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                module TEXT NOT NULL,
                progress INTEGER DEFAULT 0,
                completed INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS travel_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                route_name TEXT,
                latitude REAL,
                longitude REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )

        def add_column_if_missing(table_name, column_name, definition):
            cursor.execute(f"PRAGMA table_info({table_name})")
            existing_columns = {row[1] for row in cursor.fetchall()}
            if column_name not in existing_columns:
                cursor.execute(
                    f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}"
                )

        add_column_if_missing(
            "users", "xp", "INTEGER DEFAULT 0"
        )
        add_column_if_missing(
            "users", "level", "INTEGER DEFAULT 1"
        )
        add_column_if_missing(
            "users", "streak", "INTEGER DEFAULT 0"
        )
        add_column_if_missing(
            "users", "preparedness_level", "TEXT DEFAULT 'Beginner'"
        )
        add_column_if_missing(
            "users", "profile_photo", "TEXT"
        )

        conn.commit()

        cursor.execute(
            "INSERT OR IGNORE INTO stories (id, title, category, lesson, body, image) VALUES (?, ?, ?, ?, ?, ?)",
            (
                1,
                "Late Night Walk",
                "Safety",
                "Stay visible and connected",
                "A student learned to keep her phone charged, share her route, and remain near busy places when walking home late.",
                "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=800&q=80",
            ),
        )
        cursor.execute(
            "INSERT OR IGNORE INTO stories (id, title, category, lesson, body, image) VALUES (?, ?, ?, ?, ?, ?)",
            (
                2,
                "Safe Ride Home",
                "Travel",
                "Verify details before you go",
                "A traveler shared her location, checked the driver details, and chose to wait near a well-lit place until help arrived.",
                "https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=800&q=80",
            ),
        )
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()


init_db()


def login_required(view):
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__
    return wrapped


def get_user_by_id(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user


def get_user_contacts(user_id):
    conn = get_db()
    contacts = conn.execute(
        "SELECT * FROM emergency_contacts WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return contacts


def get_recent_alerts(user_id, limit=5):
    conn = get_db()
    alerts = conn.execute(
        "SELECT * FROM sos_alerts WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit),
    ).fetchall()
    conn.close()
    return alerts


def get_user_progress(user_id):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT xp, level, streak, preparedness_level FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        conn = get_db()
        return conn.execute(
            "SELECT xp, level, streak, preparedness_level FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    finally:
        conn.close()


def get_user_achievements(user_id):
    conn = get_db()
    achievements = conn.execute(
        "SELECT * FROM achievements WHERE user_id = ? ORDER BY earned_at DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return achievements


def get_checklist_status(user_id):
    conn = get_db()
    status = conn.execute(
        "SELECT * FROM checklist_status WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    return status


def get_user_quiz_results(user_id, limit=3):
    conn = get_db()
    results = conn.execute(
        "SELECT * FROM quiz_results WHERE user_id = ? ORDER BY submitted_at DESC LIMIT ?",
        (user_id, limit),
    ).fetchall()
    conn.close()
    return results


def compute_level(xp):
    return max(1, 1 + (xp // 100))


def compute_preparedness(xp):
    if xp >= 300:
        return "Champion"
    elif xp >= 200:
        return "Protector"
    elif xp >= 120:
        return "Explorer"
    elif xp >= 60:
        return "Learner"
    return "Beginner"


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not full_name or not email or not password or not confirm_password:
            flash("All required fields must be filled.", "error")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return redirect(url_for("register"))

        conn = get_db()
        try:
            existing = conn.execute(
                "SELECT id FROM users WHERE email = ?", (email,)
            ).fetchone()
            if existing:
                flash("Email already registered.", "error")
                return redirect(url_for("register"))

            hashed = generate_password_hash(password)
            conn.execute(
                "INSERT INTO users (full_name, email, phone, password) VALUES (?, ?, ?, ?)",
                (full_name, email, phone, hashed),
            )
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.Error as e:
            conn.rollback()
            flash(f"Database error: {e}", "error")
            return redirect(url_for("register"))
        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.", "error")
            return redirect(url_for("login"))

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]
            flash("Welcome back!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    user = get_user_by_id(session["user_id"])
    contacts = get_user_contacts(session["user_id"])
    alerts = get_recent_alerts(session["user_id"], 5)
    score = max(0, 100 - (len(alerts) * 8))
    return render_template(
        "dashboard.html",
        user=user,
        contacts=contacts,
        alerts=alerts,
        safety_score=score,
    )


@app.route("/sos")
@login_required
def sos_page():
    user = get_user_by_id(session["user_id"])
    contacts = get_user_contacts(session["user_id"])
    alerts = get_recent_alerts(session["user_id"], 6)
    return render_template("sos.html", user=user, contacts=contacts, alerts=alerts)


@app.route("/route-finder")
@login_required
def route_finder():
    user = get_user_by_id(session["user_id"])
    return render_template("route.html", user=user)


@app.route("/live-sharing")
@login_required
def live_sharing():
    user = get_user_by_id(session["user_id"])
    contacts = get_user_contacts(session["user_id"])
    return render_template("live.html", user=user, contacts=contacts)


@app.route("/contacts")
@login_required
def contacts_page():
    user = get_user_by_id(session["user_id"])
    contacts = get_user_contacts(session["user_id"])
    return render_template("contacts.html", user=user, contacts=contacts)


@app.route("/tips")
@login_required
def tips_page():
    user = get_user_by_id(session["user_id"])
    progress = get_user_progress(session["user_id"])
    achievements = get_user_achievements(session["user_id"])
    checklist = get_checklist_status(session["user_id"])
    quiz_results = get_user_quiz_results(session["user_id"])
    return render_template(
        "tips.html",
        user=user,
        progress=progress,
        achievements=achievements,
        checklist=checklist,
        quiz_results=quiz_results,
    )


@app.route("/profile")
@login_required
def profile_page():
    user = get_user_by_id(session["user_id"])
    progress = get_user_progress(session["user_id"])
    achievements = get_user_achievements(session["user_id"])
    return render_template(
        "profile.html",
        user=user,
        progress=progress,
        achievements=achievements,
    )


@app.route("/api/checklist", methods=["POST"])
@login_required
def api_checklist():
    data = request.get_json(silent=True) or {}
    fields = {
        "phone_charged": int(bool(data.get("phone_charged", False))),
        "contacts_added": int(bool(data.get("contacts_added", False))),
        "live_sharing": int(bool(data.get("live_sharing", False))),
        "sos_tested": int(bool(data.get("sos_tested", False))),
        "route_checked": int(bool(data.get("route_checked", False))),
    }

    conn = get_db()
    try:
        existing = conn.execute(
            "SELECT id FROM checklist_status WHERE user_id = ?",
            (session["user_id"],),
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE checklist_status SET phone_charged = ?, contacts_added = ?, live_sharing = ?, sos_tested = ?, route_checked = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
                (fields["phone_charged"], fields["contacts_added"], fields["live_sharing"], fields["sos_tested"], fields["route_checked"], session["user_id"]),
            )
        else:
            conn.execute(
                "INSERT INTO checklist_status (user_id, phone_charged, contacts_added, live_sharing, sos_tested, route_checked) VALUES (?, ?, ?, ?, ?, ?)",
                (session["user_id"], fields["phone_charged"], fields["contacts_added"], fields["live_sharing"], fields["sos_tested"], fields["route_checked"]),
            )
        conn.commit()
        return jsonify({"success": True, "message": "Checklist updated."})
    except sqlite3.Error:
        conn.rollback()
        return jsonify({"success": False, "message": "Could not update checklist."}), 500
    finally:
        conn.close()


@app.route("/api/quiz", methods=["POST"])
@login_required
def api_quiz():
    data = request.get_json(silent=True) or {}
    score = int(data.get("score", 0))
    total = int(data.get("total", 0))
    xp_earned = max(5, int((score / total) * 30)) if total else 0

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO quiz_results (user_id, score, total, xp_earned) VALUES (?, ?, ?, ?)",
            (session["user_id"], score, total, xp_earned),
        )
        user = conn.execute(
            "SELECT xp, level FROM users WHERE id = ?",
            (session["user_id"],),
        ).fetchone()
        if user:
            new_xp = user["xp"] + xp_earned
            new_level = compute_level(new_xp)
            new_preparedness = compute_preparedness(new_xp)
            conn.execute(
                "UPDATE users SET xp = ?, level = ?, preparedness_level = ? WHERE id = ?",
                (new_xp, new_level, new_preparedness, session["user_id"]),
            )
        conn.commit()

        if score >= 80:
            award = {
                "title": "Safety Learner",
                "description": "Completed a strong safety quiz.",
                "icon": "🏆",
            }
            conn.execute(
                "INSERT OR IGNORE INTO achievements (user_id, title, description, icon) VALUES (?, ?, ?, ?)",
                (session["user_id"], award["title"], award["description"], award["icon"]),
            )
        conn.commit()
        return jsonify(
            {
                "success": True,
                "message": "Quiz result saved.",
                "xp_earned": xp_earned,
            }
        )
    except sqlite3.Error:
        conn.rollback()
        return jsonify({"success": False, "message": "Could not save quiz result."}), 500
    finally:
        conn.close()


@app.route("/api/achievements")
@login_required
def api_achievements():
    return jsonify(
        [
            dict(item)
            for item in get_user_achievements(session["user_id"])
        ]
    )


@app.route("/api/stories")
@login_required
def api_stories():
    conn = get_db()
    stories = conn.execute(
        "SELECT * FROM stories ORDER BY id"
    ).fetchall()
    conn.close()
    return jsonify([dict(story) for story in stories])


@app.route("/api/contacts", methods=["GET", "POST"])
@login_required
def api_contacts():
    user_id = session["user_id"]
    if request.method == "GET":
        contacts = get_user_contacts(user_id)
        return jsonify([dict(contact) for contact in contacts])

    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    relation = (data.get("relation") or "").strip()

    if not name or not phone:
        return jsonify({"success": False, "message": "Name and phone are required."}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO emergency_contacts (user_id, name, phone, relation) VALUES (?, ?, ?, ?)",
        (user_id, name, phone, relation),
    )
    conn.commit()
    contact_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()[0]
    conn.close()

    return jsonify({"success": True, "id": contact_id, "message": "Contact added successfully."})


@app.route("/api/contacts/<int:contact_id>", methods=["GET", "PUT", "DELETE"])
@login_required
def api_contact_detail(contact_id):
    user_id = session["user_id"]
    conn = get_db()
    contact = conn.execute(
        "SELECT * FROM emergency_contacts WHERE id = ? AND user_id = ?",
        (contact_id, user_id),
    ).fetchone()

    if not contact:
        conn.close()
        return jsonify({"success": False, "message": "Contact not found."}), 404

    if request.method == "GET":
        conn.close()
        return jsonify(dict(contact))

    if request.method == "PUT":
        data = request.get_json(silent=True) or {}
        name = (data.get("name") or "").strip()
        phone = (data.get("phone") or "").strip()
        relation = (data.get("relation") or "").strip()

        if not name or not phone:
            conn.close()
            return jsonify({"success": False, "message": "Name and phone are required."}), 400

        conn.execute(
            "UPDATE emergency_contacts SET name = ?, phone = ?, relation = ? WHERE id = ?",
            (name, phone, relation, contact_id),
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Contact updated successfully."})

    conn.execute("DELETE FROM emergency_contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Contact deleted successfully."})


@app.route("/api/sos", methods=["POST"])
@login_required
def api_sos():
    data = request.get_json(silent=True) or {}
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    message = (data.get("message") or "Emergency SOS alert triggered.").strip()

    if latitude is None or longitude is None:
        return jsonify({"success": False, "message": "Location coordinates are required."}), 400

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO sos_alerts (user_id, latitude, longitude, message) VALUES (?, ?, ?, ?)",
            (session["user_id"], latitude, longitude, message),
        )
        alert_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()[0]

        # record the main emergency message
        conn.execute(
            "INSERT INTO emergency_messages (user_id, message, latitude, longitude) VALUES (?, ?, ?, ?)",
            (session["user_id"], message, latitude, longitude),
        )
        emergency_msg_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()[0]

        # Notify contacts by recording an entry per contact in emergency_history
        contacts = conn.execute(
            "SELECT name, phone, relation FROM emergency_contacts WHERE user_id = ?",
            (session["user_id"],),
        ).fetchall()
        recipients = []
        for c in contacts:
            name = c[0]
            phone = c[1]
            relation = c[2]
            status = 'Prepared'
            conn.execute(
                "INSERT INTO emergency_history (user_id, contact_name, contact_phone, relation, method, status, alert_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (session["user_id"], name, phone, relation, 'sms', status, alert_id),
            )
            recipients.append({"name": name, "phone": phone, "relation": relation, "status": status})

        conn.execute(
            "INSERT OR IGNORE INTO checklist_status (user_id) VALUES (?)",
            (session["user_id"],),
        )
        conn.execute(
            "UPDATE checklist_status SET sos_tested = 1, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
            (session["user_id"],),
        )
        conn.commit()
        return jsonify(
            {
                "success": True,
                "message": "Emergency alert recorded successfully.",
                "alert_text": message,
                "recipients": recipients,
            }
        )
    except sqlite3.Error:
        conn.rollback()
        return jsonify({"success": False, "message": "Unable to save SOS alert."}), 500
    finally:
        conn.close()


@app.route('/api/share_live', methods=['POST'])
@login_required
def api_share_live():
    data = request.get_json(silent=True) or {}
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    method = data.get('method') or 'link'
    recipients = data.get('recipients') or []

    if latitude is None or longitude is None:
        return jsonify({'success': False, 'message': 'Latitude and longitude are required.'}), 400

    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO live_sharing_history (user_id, latitude, longitude, method, recipients, status) VALUES (?, ?, ?, ?, ?, ?)',
            (session['user_id'], latitude, longitude, method, ','.join(recipients) if isinstance(recipients, list) else str(recipients), 'shared'),
        )
        share_id = conn.execute('SELECT last_insert_rowid() AS id').fetchone()[0]
        conn.commit()
        share_url = url_for('shared', share_id=share_id, _external=True)
        return jsonify({'success': True, 'share_id': share_id, 'share_url': share_url})
    except sqlite3.Error:
        conn.rollback()
        return jsonify({'success': False, 'message': 'Unable to save share session.'}), 500
    finally:
        conn.close()


@app.route('/api/share_history')
@login_required
def api_share_history():
    conn = get_db()
    rows = conn.execute('SELECT * FROM live_sharing_history WHERE user_id = ? ORDER BY created_at DESC', (session['user_id'],)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/qr')
@login_required
def api_qr():
    target = request.args.get('url', '').strip()
    if not target:
        return jsonify({'success': False, 'message': 'URL required.'}), 400
    img = qrcode.make(target)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    data = base64.b64encode(buf.getvalue()).decode('ascii')
    return jsonify({'success': True, 'image': f'data:image/png;base64,{data}'})


@app.route('/api/route-plan', methods=['POST'])
@login_required
def api_route_plan():
    data = request.get_json(silent=True) or {}
    start = data.get('start') or {}
    destination = data.get('destination') or {}
    route_type = (data.get('route_type') or 'fastest').lower()

    def normalize_point(point):
        if isinstance(point, dict):
            lat = point.get('lat')
            lng = point.get('lng')
            if lat is None or lng is None:
                return None
            return {'lat': float(lat), 'lng': float(lng)}
        return None

    start_point = normalize_point(start)
    dest_point = normalize_point(destination)
    if not start_point or not dest_point:
        return jsonify({'success': False, 'message': 'Start and destination coordinates are required.'}), 400

    route_url = f"https://router.project-osrm.org/route/v1/driving/{start_point['lng']},{start_point['lat']};{dest_point['lng']},{dest_point['lat']}?overview=full&geometries=geojson&alternatives=true"
    try:
        response = requests.get(route_url, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        return jsonify({'success': False, 'message': 'Routing service unavailable.'}), 502

    routes = payload.get('routes', [])
    if not routes:
        return jsonify({'success': False, 'message': 'No route found.'}), 404

    if route_type == 'safest':
        selected = max(routes, key=lambda r: r.get('distance', 0) / max(1, r.get('duration', 1)))
    else:
        selected = min(routes, key=lambda r: r.get('duration', 0))

    risk_score = max(25, min(96, 70 - int(selected.get('distance', 0) / 1000) + (5 if route_type == 'safest' else 0)))
    return jsonify({
        'success': True,
        'route_type': route_type,
        'distance': round(selected.get('distance', 0) / 1000, 2),
        'duration': round(selected.get('duration', 0) / 60, 1),
        'risk_score': risk_score,
        'geometry': selected.get('geometry'),
        'start': start_point,
        'destination': dest_point,
    })


@app.route('/api/safety-progress', methods=['GET', 'POST'])
@login_required
def api_safety_progress():
    user_id = session['user_id']
    if request.method == 'GET':
        conn = get_db()
        row = conn.execute('SELECT * FROM safety_progress WHERE user_id = ?', (user_id,)).fetchone()
        conn.close()
        return jsonify(dict(row) if row else {'xp': 0, 'level': 1, 'weekly_progress': 0, 'monthly_progress': 0})

    data = request.get_json(silent=True) or {}
    xp = int(data.get('xp', 0))
    level = int(data.get('level', 1))
    weekly = int(data.get('weekly_progress', 0))
    monthly = int(data.get('monthly_progress', 0))
    conn = get_db()
    try:
        conn.execute('INSERT OR IGNORE INTO safety_progress (user_id) VALUES (?)', (user_id,))
        conn.execute('UPDATE safety_progress SET xp = ?, level = ?, weekly_progress = ?, monthly_progress = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?', (xp, level, weekly, monthly, user_id))
        conn.commit()
        return jsonify({'success': True, 'message': 'Progress saved.'})
    finally:
        conn.close()


@app.route('/api/challenges', methods=['GET', 'POST'])
@login_required
def api_challenges():
    user_id = session['user_id']
    if request.method == 'GET':
        conn = get_db()
        rows = conn.execute('SELECT * FROM daily_challenges WHERE user_id = ? ORDER BY id DESC', (user_id,)).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])

    data = request.get_json(silent=True) or {}
    title = (data.get('title') or '').strip()
    completed = int(bool(data.get('completed', False)))
    xp_earned = int(data.get('xp_earned', 0))
    conn = get_db()
    try:
        conn.execute('INSERT INTO daily_challenges (user_id, title, completed, xp_earned, completed_at) VALUES (?, ?, ?, ?, ?)', (user_id, title, completed, xp_earned, datetime.now().strftime('%Y-%m-%d %H:%M:%S') if completed else None))
        conn.commit()
        return jsonify({'success': True, 'message': 'Challenge updated.'})
    finally:
        conn.close()


@app.route('/api/learning-progress', methods=['GET', 'POST'])
@login_required
def api_learning_progress():
    user_id = session['user_id']
    if request.method == 'GET':
        conn = get_db()
        rows = conn.execute('SELECT * FROM learning_progress WHERE user_id = ? ORDER BY updated_at DESC', (user_id,)).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])

    data = request.get_json(silent=True) or {}
    module = (data.get('module') or '').strip()
    progress = int(data.get('progress', 0))
    completed = int(bool(data.get('completed', False)))
    conn = get_db()
    try:
        conn.execute('INSERT OR IGNORE INTO learning_progress (user_id, module) VALUES (?, ?)', (user_id, module))
        conn.execute('UPDATE learning_progress SET progress = ?, completed = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ? AND module = ?', (progress, completed, user_id, module))
        conn.commit()
        return jsonify({'success': True, 'message': 'Learning progress updated.'})
    finally:
        conn.close()


@app.route('/api/travel-history', methods=['POST'])
@login_required
def api_travel_history():
    data = request.get_json(silent=True) or {}
    route_name = (data.get('route_name') or '').strip()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    conn = get_db()
    try:
        conn.execute('INSERT INTO travel_history (user_id, route_name, latitude, longitude) VALUES (?, ?, ?, ?)', (session['user_id'], route_name, latitude, longitude))
        conn.commit()
        return jsonify({'success': True, 'message': 'Travel history saved.'})
    finally:
        conn.close()


@app.route('/shared/<int:share_id>')
def shared(share_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM live_sharing_history WHERE id = ?', (share_id,)).fetchone()
    conn.close()
    if not row:
        return 'Share link not found.', 404
    # render a simple page that redirects to google maps and also shows OSM link
    return render_template('shared.html', share=row)


@app.route("/api/profile", methods=["POST"])
@login_required
def api_profile():
    user_id = session["user_id"]
    full_name = request.form.get("full_name", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()

    if not full_name:
        flash("Name is required.", "error")
        return redirect(url_for("profile_page"))

    conn = get_db()
    try:
        conn.execute(
            "UPDATE users SET full_name = ?, phone = ?, address = ? WHERE id = ?",
            (full_name, phone, address, user_id),
        )
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        flash("Unable to update profile.", "error")
        return redirect(url_for("profile_page"))
    finally:
        conn.close()

    session["user_name"] = full_name
    flash("Profile updated successfully.", "success")
    return redirect(url_for("profile_page"))
@app.route("/test-supabase")
def test_supabase():
    try:
        client = get_supabase_client()
        response = client.table("users").select("*").execute()

        return {
            "status": "success",
            "message": "Supabase is connected!",
            "data": response.data or []
        }

    except SupabaseUnavailableError as exc:
        return {
            "status": "degraded",
            "message": str(exc)
        }, 503
    except Exception as exc:
        return {
            "status": "error",
            "message": "Supabase is temporarily unavailable. Please try again shortly."
        }, 503


if __name__ == "__main__":
    app.run(debug=True)
