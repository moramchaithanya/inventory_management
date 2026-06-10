from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():

    conn = get_db()

    products = conn.execute(
        "SELECT * FROM products"
    ).fetchall()

    total_products = len(products)

    total_stock = sum(
        product["quantity"]
        for product in products
    )

    total_value = sum(
        product["quantity"] * product["price"]
        for product in products
    )

    conn.close()

    return render_template(
        "index.html",
        products=products,
        total_products=total_products,
        total_stock=total_stock,
        total_value=total_value
    )

@app.route('/add', methods=['GET', 'POST'])
def add_product():

    if request.method == 'POST':

        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']

        conn = get_db()

        conn.execute(
            "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
            (name, quantity, price)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_product.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):

    conn = get_db()

    if request.method == 'POST':

        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']

        conn.execute(
            "UPDATE products SET name=?, quantity=?, price=? WHERE id=?",
            (name, quantity, price, id)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    product = conn.execute(
        "SELECT * FROM products WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        'edit_product.html',
        product=product
    )

@app.route('/delete/<int:id>')
def delete_product(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM products WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)