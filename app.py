from flask import Flask, request, render_template, render_template_string, redirect, url_for
from datetime import datetime

app = Flask(__name__)
visitors = []

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users")
def users():
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    visitors.append({
        "ip": ip,
        "ua": user_agent,
        "time": time
    })

    html = """
    <h1>訪客紀錄</h1>
    <table border="1">
        <tr>
            <th>IP</th>
            <th>User-Agent</th>
            <th>時間</th>
        </tr>
        {% for v in visitors %}
        <tr>
            <td>{{ v.ip }}</td>
            <td>{{ v.ua }}</td>
            <td>{{ v.time }}</td>
        </tr>
        {% endfor %}
    </table>
    """

    return render_template_string(html, visitors=visitors)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # ⚠️ 故意的弱密碼（CTF 教學）
        if username == "vincent" and password == "1234":
            message = "Login success! FLAG{weak_password}"

        elif username == "vincent" and password == "20120315":
            return redirect(url_for("users"))

        else:
            message = "帳號或密碼錯誤"

    return render_template("login.html", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
