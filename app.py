from flask import Flask, request, render_template, redirect, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"   # required for session

# ---------- DATABASE CONNECTION ----------
def get_db():
    conn = sqlite3.connect("requests.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- USER FORM ----------
@app.route("/")
def form():
    return render_template("form.html")

# ---------- FORM SUBMISSION ----------
@app.route("/submit_request", methods=["POST"])
def submit_request():
    name = request.form.get("name")
    email = request.form.get("email")
    request_type = request.form.get("request_type")
    message = request.form.get("message")

    if not name or not email:
        return "Name and Email are required!"

    conn = get_db()
    conn.execute(
        "INSERT INTO requests (name, email, request_type, message) VALUES (?, ?, ?, ?)",
        (name, email, request_type, message)
    )
    conn.commit()
    conn.close()

    return redirect("/success")

# ---------- SUCCESS PAGE ----------
@app.route("/success")
def success():
    return render_template("success.html")

# ---------- ADMIN LOGIN ----------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            return "Invalid username or password"

    return render_template("admin_login.html")

# ---------- ADMIN DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/admin")

    conn = get_db()
    rows = conn.execute("SELECT * FROM requests").fetchall()
    conn.close()

    return render_template("dashboard.html", requests=rows)

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/admin")

# ---------- API (OPTIONAL) ----------
@app.route("/api/requests")
def api_requests():
    conn = get_db()
    rows = conn.execute("SELECT * FROM requests").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

