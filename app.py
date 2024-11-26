import os
import re
import json
import secrets
import hmac
import datetime
from functools import wraps

from flask import Flask, request, redirect, render_template_string, jsonify, abort, session, url_for, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

RESERVED_PATHS = [
    "login",
    "logout",
    "dashboard",
]

app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))

URLS_PATH = os.environ.get("SHOR10_URLS", "urls.json")
ADMIN_PASSWORD = os.environ.get("SHOR10_PASSWORD")
if not ADMIN_PASSWORD:
    raise SystemExit("SHOR10_PASSWORD env var not set, it's impossible to submit links!")

def load_urls():
    if os.path.exists(URLS_PATH):
        with open(URLS_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_urls(urls):
    with open(URLS_PATH, 'w') as f:
        json.dump(urls, f, indent=4)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))  # Redirect to the login page if not logged in
        return f(*args, **kwargs)
    return decorated_function

def is_valid_input(value: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', value))

# Route to handle login and URL shortening
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect('/shorten')

    if request.method == 'POST':
        entered_password = request.form.get('password')
        if hmac.compare_digest(entered_password, ADMIN_PASSWORD):
            session['logged_in'] = True
            return redirect('/')
        else:
            return "Invalid password!", 403

    return render_template("login.html")

@app.route('/', methods=['GET', 'POST'])
@login_required
def shorten():
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        if not long_url:
            abort(400, description="long_url required")
        short_id = request.form.get('short_id') or secrets.token_urlsafe(4)
        if short_id in RESERVED_PATHS:
            abort(400, description=f"Cannot use {short_id} as a short code")

        urls = load_urls()

        if short_id in urls:
            abort(400, description=f"{short_id} is already in use")

        if not is_valid_input(short_id):
            abort(400, description=f"{short_id} contains invalid characters")

        created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        urls[short_id] = {
            'long_url': long_url,
            'click_count': 0,
            'created_at': created_at,
            'last_visited': None
        }

        save_urls(urls)

        return redirect(url_for("dashboard"))

    # Form to shorten a URL
    return render_template("index.html")

# Route to view URL statistics (optional)
@app.route('/dashboard')
@login_required
def dashboard():
    if not session.get('logged_in'):
        return redirect('/login')  # Redirect to login if not logged in

    urls = load_urls()

    if not urls:
        return render_template_string('''
        <h1>Dashboard</h1>
        <p>No URLs have been shortened yet.</p>
        <a href="/shorten">Shorten a URL</a>
        ''')

    return render_template("dashboard.html", urls=urls)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect('/login')

@app.route('/<short_id>')
def redirect_to_long_url(short_id):
    urls = load_urls()
    url_info = urls.get(short_id)

    if not url_info:
        return 'Short URL not found', 404

    url_info['click_count'] += 1
    url_info['last_visited'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    save_urls(urls)

    return redirect(url_info['long_url'])

if __name__ == '__main__':
    app.run(debug=True)
