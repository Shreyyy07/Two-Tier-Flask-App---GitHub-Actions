from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            users.append(name)
        return redirect("/")
    
    return render_template("index.html", users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)