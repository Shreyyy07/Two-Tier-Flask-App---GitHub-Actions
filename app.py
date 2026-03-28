from flask import Flask, render_template, request, redirect
import mysql.connector
import time

app = Flask(__name__)

# 🔹 DB Connection with retry
def get_db_connection():
    for i in range(20):
        try:
            db = mysql.connector.connect(
                host="mysql",
                user="root",
                password="root",
                database="testdb"
            )
            return db
        except:
            print("MySQL not ready, retrying...")
            time.sleep(2)
    raise Exception("Database not ready")


# 🔹 HOME ROUTE
@app.route("/", methods=["GET", "POST"])
def home():
    db = get_db_connection()
    cursor = db.cursor()

    # ➤ Add Task
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            cursor.execute(
                "INSERT INTO users (task, completed) VALUES (%s, %s)",
                (task, False)
            )
            db.commit()
        return redirect("/")

    # ➤ Fetch Tasks
    cursor.execute("SELECT id, task, completed FROM users")
    tasks = cursor.fetchall()

    # ➤ Stats
    total = len(tasks)
    completed = sum(1 for t in tasks if t[2])
    pending = total - completed

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending
    )


# 🔹 COMPLETE TASK
@app.route("/complete/<int:id>")
def complete(id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE users SET completed = TRUE WHERE id = %s",
        (id,)
    )
    db.commit()

    return redirect("/")


# 🔹 DELETE TASK
@app.route("/delete/<int:id>")
def delete(id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    db.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)