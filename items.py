from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/collection")
def collection():
    return render_template("collection.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# 🔥 DATABASE FUNCTION (FIXED)
def get_items():
    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()

    # match your table + columns
    cursor.execute("SELECT Product_Name, Image FROM Product")

    items = cursor.fetchall()
    conn.close()

    return [
        {
            "name": item[0],
            "image": "/static/" + item[1]   # 🔥 IMPORTANT
        }
        for item in items
    ]

# API
@app.route("/items")
def items():
    return jsonify(get_items())

if __name__ == "__main__":
    app.run(debug=True)