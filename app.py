from flask import Flask, request, render_template, render_template_string, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
visitors = []

# ✅ 全站訪客紀錄（只記一次）
@app.before_request
def log_visit():
    visitors.append({
        "ip": request.remote_addr,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ua": request.headers.get("User-Agent")
    })

@app.route("/")
def index():
    return render_template("index.html")

# ✅ 一般訪客可看到的紀錄頁（美化版）
@app.route("/visit")
def show_visit():
    return render_template("visit.html", visitors=visitors)

# ⚠️ 管理頁（CTF 洩漏點）
@app.route("/users")
def users():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Admin Logs</title>
        <style>
            body {
                background: black;
                color: #00ff88;
                font-family: Consolas;
                padding: 30px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border-bottom: 1px solid #00ff88;
                padding: 8px;
            }
            h1 {
                color: #00ff88;
            }
            .flag {
                margin-top: 20px;
                color: #ff5555;
                font-weight: bold;
            }
            a {
                color: #00ff88;
            }
        </style>
    </head>
    <body>

    <h1>⚠ Admin Visitor Logs</h1>

    <table>
        <tr>
            <th>IP</th>
            <th>User-Agent</th>
            <th>Time</th>
        </tr>
        {% for v in visitors %}
        <tr>
            <td>{{ v.ip }}</td>
            <td>{{ v.ua }}</td>
            <td>{{ v.time }}</td>
        </tr>
        {% endfor %}
    </table>

    <div class="flag">
        FLAG{admin_page_leak}
    </div>

    <a href="/">← 回首頁</a>

    </body>
    </html>
    """
    return render_template_string(html, visitors=visitors)

# ✅ 弱登入（CTF 用）
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "vincent" and password == "1234":
            return redirect(url_for("xss_lab"))

        elif username == "vincent" and password == "123456":
            return redirect(url_for("show_visit"))

        else:
            message = "帳號或密碼錯誤"

    return render_template("login.html", message=message)


# =====================
# XSS LAB
# =====================

xss_comments = []


@app.route("/xss", methods=["GET", "POST"])
def xss_lab():
    content = ""
    if request.method == "POST":
        content = request.form.get("content", "")
    return render_template("XSS.html", content=content)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
