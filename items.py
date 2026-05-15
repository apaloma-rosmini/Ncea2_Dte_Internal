# Imports Flask and Sqlite3
from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

# HTML Routes

# Home.html
@app.route("/") 
def home():
    return render_template("home.html")

# Collection.html
@app.route("/collection")
def collection():
    return render_template("collection.html")

# Product.HTML
@app.route("/product/<int:id>")
def product_page(id):

    conn = get_db_connection()

    product = conn.execute("""
        SELECT * FROM Product
        WHERE Product_ID = ?
    """, (id,)).fetchone()

    conn.close()

    # If product does not exist
    if product is None:
        return render_template("404.html"), 404

    return render_template("product.html", product_id=id)


# Cart.html
@app.route("/cart")
def cart():
    return render_template("cart.html")


# Checkout.html
@app.route("/checkout")
def checkout():
    return render_template("checkout.html")



# Database Connection

def get_db_connection():
    conn = sqlite3.connect("items.db")
    conn.row_factory = sqlite3.Row
    return conn

# Products
@app.route("/items")
def items():
    conn = get_db_connection()

# Gets ID from database
    items = conn.execute("""
        SELECT Product_ID, Product_Name, Image, Product_Price, Product_Type
        FROM Product
    """).fetchall()


    conn.close()

# Creates a dictionary
    return jsonify([
        {
            
            "id": item["Product_ID"],
            "name": item["Product_Name"],
            "image": "/static/" + item["Image"], # File path
            "price": item["Product_Price"],
            "type": item["Product_Type"]

        }
        for item in items
    ])



# Individual items based on ID
@app.route("/item/<int:id>")
def single_item(id):
    conn = get_db_connection()


    item = conn.execute("""
        SELECT * FROM Product WHERE Product_ID = ?
    """, (id,)).fetchone()


    conn.close()



# Prints error if item not found
    if item is None:
        return jsonify({"error": "Item not found"}), 404




# If found the items are returned to the dictionary
    return jsonify({

        "id": item["Product_ID"],
        "name": item["Product_Name"],
        "image": "/static/" + item["Image"],
        "price": item["Product_Price"],
        "type": item["Product_Type"],
        "description": item["Description"]

    })


#Running for debug
if __name__ == "__main__":
    app.run(debug=True)

#For running error Page if user encoutners error
@app.errorhandler(404)
def page_not_found(e):
    # This catches global "Route Not Found" errors
    return render_template("404.html"), 404