from flask import Flask, render_template, request, redirect
import mysql.connector
import time

app = Flask(__name__)

# 🔹 Retry connection until MySQL is ready
def get_db_connection():
    for i in range(20):
        try:
            db = mysql.connector.connect(
                host="mysql",
                user="root",
                password="root",
                database="testdb"
            )
            print("Connected to MySQL ✅")
            return db
        except Exception as e:
            print("MySQL not ready, retrying...")
            time.sleep(2)
    raise Exception("Database not ready after retries ❌")


# 🔹 Initialize DB (CREATE TABLE)
def init_db():
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255)
    )
    """)

    db.commit()
    cursor.close()
    db.close()
    print("Database initialized ✅")


# 🔹 Call once when app starts
init_db()


@app.route("/", methods=["GET", "POST"])
def home():
    db = get_db_connection()
    cursor = db.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        if name:
            cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            db.commit()
        return redirect("/")

    cursor.execute("SELECT name FROM users")
    users = cursor.fetchall()
    users = [user[0] for user in users]

    cursor.close()
    db.close()

    return render_template("index.html", users=users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)