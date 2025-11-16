from flask import Flask, render_template, request, redirect, url_for, session, g, flash, send_file
import sqlite3, os
from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

# ------------------ PATHS ------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# ------------------ DATABASE HELPERS ------------------

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_app_db():
    if not os.path.exists(DB_PATH):
        print("→ Creating database...")
        from init_db import init_db
        init_db(DB_PATH)
    else:
        print("→ Database already exists.")

# ------------------ FLASK APP SETUP ------------------

app = Flask(__name__)
app.secret_key = "dev-secret-key"
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'images')

# Initialize DB once at startup
init_app_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# ------------------ ROUTES ------------------

@app.route('/')
def index():
    cakes = query_db("SELECT * FROM cakes")
    return render_template('index.html', cakes=cakes)

# ---------- ADMIN LOGIN ----------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = query_db('SELECT * FROM admins WHERE username=? AND password=?', (username, password), one=True)
        if admin:
            session['admin'] = admin['id']
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('admin_login.html')

# ---------- ADMIN DASHBOARD ----------
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    cakes = query_db("SELECT * FROM cakes")
    orders = query_db("SELECT * FROM orders")
    return render_template('admin_dashboard.html', cakes=cakes, orders=orders)

# ---------- ADD CAKE ----------
@app.route('/admin/add_cake', methods=['GET', 'POST'])
def add_cake():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        filename = ""
        f = request.files.get('image')
        if f and f.filename:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db = get_db()
        db.execute("INSERT INTO cakes (name, price, image) VALUES (?,?,?)", (name, price, filename))
        db.commit()
        flash('Cake added', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_cake.html')

# ---------- EDIT CAKE ----------
@app.route('/admin/edit_cake/<int:cake_id>', methods=['GET', 'POST'])
def edit_cake(cake_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    cake = query_db("SELECT * FROM cakes WHERE id=?", (cake_id,), one=True)
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        filename = cake['image']
        f = request.files.get('image')
        if f and f.filename:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db = get_db()
        db.execute("UPDATE cakes SET name=?, price=?, image=? WHERE id=?", (name, price, filename, cake_id))
        db.commit()
        flash('Cake updated successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_cake.html', cake=cake)

# ---------- DELETE CAKE ----------
@app.route('/admin/delete_cake/<int:cake_id>')
def delete_cake(cake_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    db = get_db()
    db.execute("DELETE FROM cakes WHERE id=?", (cake_id,))
    db.commit()
    flash('Cake deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# ---------- CAKES PAGE ----------
@app.route('/cakes')
def cakes_page():
    cakes = query_db("SELECT * FROM cakes")
    return render_template('cakes.html', cakes=cakes)

# ---------- CART ----------
@app.route('/cart/add/<int:cake_id>')
def add_to_cart(cake_id):
    cart = session.get('cart', {})
    cart[str(cake_id)] = cart.get(str(cake_id), 0) + 1
    session['cart'] = cart
    flash('Added to cart', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for cid, qty in cart.items():
        cake = query_db("SELECT * FROM cakes WHERE id=?", (cid,), one=True)
        if cake:
            subtotal = cake['price'] * qty
            items.append({'cake': cake, 'qty': qty, 'subtotal': subtotal})
            total += subtotal
    return render_template('cart.html', items=items, total=total)

@app.route('/cart/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Cart empty', 'warning')
        return redirect(url_for('index'))
    db = get_db()
    total = float(request.form.get('total', 0))
    db.execute("INSERT INTO orders (items, total) VALUES (?,?)", (str(cart), total))
    db.commit()
    order_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    session['cart'] = {}
    flash('Order placed — demo only', 'success')
    return redirect(url_for('download_bill', order_id=order_id))

# ---------- USER REGISTER ----------
@app.route('/user/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        db.execute("INSERT INTO users (username,password) VALUES (?,?)", (username, password))
        db.commit()
        flash('Registered — now login', 'success')
        return redirect(url_for('user_login'))
    return render_template('register.html')

# ---------- USER LOGIN ----------
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM users WHERE username=? AND password=?', (username, password), one=True)
        if user:
            session['user'] = user['id']
            return redirect(url_for('index'))
        flash('Invalid credentials', 'danger')
    return render_template('user_login.html')

# ---------- BILL PDF DOWNLOAD ----------
@app.route('/bill/<int:order_id>')
def download_bill(order_id):
    order = query_db("SELECT * FROM orders WHERE id=?", (order_id,), one=True)
    if not order:
        flash("Bill not found", "danger")
        return redirect(url_for('index'))

    # Create PDF in memory
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(400,600))
    width, height = 400, 600
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-50, "🍰 Cake Shop 🍰")
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height-80, "BILL RECEIPT")
    c.setFont("Helvetica", 12)
    c.drawString(30, height-120, f"Order ID: {order['id']}")
    c.drawString(30, height-140, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}")

    # Items
    items = eval(order['items'])  # stored as string
    y = height-180
    c.drawString(30, y, "----------------------------------------")
    y -= 20
    for cid, qty in items.items():
        cake = query_db("SELECT * FROM cakes WHERE id=?", (cid,), one=True)
        if cake:
            line = f"{cake['name']:<20} {qty} × {cake['price']} = {cake['price']*qty}"
            c.drawString(30, y, line)
            y -= 20
    c.drawString(30, y, "----------------------------------------")
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, y, f"TOTAL PAYABLE: ₹{order['total']}")
    c.showPage()
    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"bill_{order['id']}.pdf", mimetype='application/pdf')


# ------------------ RUN APP ------------------
if __name__ == '__main__':
    app.run(debug=True)
