from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/collection")
def collection():
    return render_template("collection.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/product/<int:id>")
def product_page(id):
    return render_template("product.html", product_id=id)


# ---------- DATABASE ----------
def get_db_connection():
    conn = sqlite3.connect("items.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- ALL ITEMS ----------
@app.route("/items")
def items():
    try:
        conn = get_db_connection()

        items = conn.execute("""
            SELECT Product_ID, Product_Name, Image, Product_Price, Product_Type
            FROM Product
        """).fetchall()

        conn.close()

        return jsonify([
            {
                "id": item["Product_ID"],
                "name": item["Product_Name"],
                "image": "/static/" + item["Image"] if item["Image"] else "",
                "price": item["Product_Price"],
                "type": item["Product_Type"]
            }
            for item in items
        ])

    except Exception as e:
        print("ERROR /items:", e)
        return jsonify([])


# ---------- SINGLE PRODUCT ----------
@app.route("/item/<int:id>")
def single_item(id):
    try:
        conn = get_db_connection()

        item = conn.execute("""
            SELECT * FROM Product WHERE Product_ID = ?
        """, (id,)).fetchone()

        conn.close()

        # 🔥 Prevent crash if item doesn't exist
        if item is None:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({
            "id": item["Product_ID"],
            "name": item["Product_Name"],
            "image": "/static/" + item["Image"] if item["Image"] else "",
            "price": item["Product_Price"],
            "type": item["Product_Type"],
            "description": item["Description"] if item["Description"] else ""
        })

    except Exception as e:
        print("ERROR /item:", e)
        return jsonify({"error": "Server error"}), 500


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")