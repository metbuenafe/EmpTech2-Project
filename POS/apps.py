from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('pos_water.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/products', methods=['GET', 'POST'])
def products():
    conn = get_db()
    if request.method == 'POST':
        name = request.form['name']
        size = request.form['size']
        price = request.form['price']
        conn.execute('INSERT INTO products (name, size, price) VALUES (?, ?, ?)', (name, size, price))
        conn.commit()
        return redirect(url_for('products'))
    products = conn.execute('SELECT * FROM products').fetchall()
    return render_template('products.html', products=products)

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    conn = get_db()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        conn.execute('INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)', (name, phone, address))
        conn.commit()
        return redirect(url_for('customers'))
    customers = conn.execute('SELECT * FROM customers').fetchall()
    return render_template('customers.html', customers=customers)

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    conn = get_db()
    products = conn.execute('SELECT * FROM products').fetchall()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        conn.execute('INSERT INTO orders (customer_id) VALUES (?)', (customer_id,))
        order_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        for product in products:
            qty = int(request.form.get(f'qty_{product["id"]}', 0))
            if qty > 0:
                conn.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)', (order_id, product["id"], qty))
        conn.commit()
        return redirect(url_for('orders'))
    orders = conn.execute('SELECT * FROM orders').fetchall()
    return render_template('orders.html', products=products, customers=customers, orders=orders)

@app.route('/inventory')
def inventory():
    conn = get_db()
    products = conn.execute('SELECT * FROM products').fetchall()
    return render_template('inventory.html', products=products)

@app.route('/delivery', methods=['GET', 'POST'])
def delivery():
    conn = get_db()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    if request.method == 'POST':
        order_id = request.form['order_id']
        delivery_person = request.form['delivery_person']
        conn.execute('INSERT INTO deliveries (order_id, delivery_person) VALUES (?, ?)', (order_id, delivery_person))
        conn.commit()
        return redirect(url_for('delivery'))
    deliveries = conn.execute('SELECT * FROM deliveries').fetchall()
    return render_template('delivery.html', deliveries=deliveries, orders=orders)

@app.route('/reports')
def reports():
    # Placeholder for your reporting logic
    return render_template('reports.html')

if __name__ == '__main__':
    app.run(debug=True)# POS/__init__.py
# POS/apps.py