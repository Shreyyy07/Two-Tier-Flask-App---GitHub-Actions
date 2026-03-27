from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="mysql",              # VERY IMPORTANT (service name)
    user="root",
    password="root",
    database="testdb"
)

cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
)
""")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            db.commit()
        return redirect("/")

    cursor.execute("SELECT name FROM users")
    users = cursor.fetchall()

    # Convert list of tuples → simple list
    users = [user[0] for user in users]

    return render_template("index.html", users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)