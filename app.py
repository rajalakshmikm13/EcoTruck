from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ecotruck-college-project-key")
DB = os.path.join(os.path.dirname(__file__), "ecotruck.db")

CATEGORIES = ["Organic", "Plastic", "Paper", "Metal", "E-waste", "Mixed Waste"]

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
          email TEXT UNIQUE NOT NULL, password TEXT NOT NULL,
          role TEXT NOT NULL DEFAULT 'citizen', phone TEXT DEFAULT '',
          address TEXT DEFAULT '', created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS trucks(
          id INTEGER PRIMARY KEY AUTOINCREMENT, plate TEXT UNIQUE NOT NULL,
          model TEXT NOT NULL, capacity REAL NOT NULL, status TEXT DEFAULT 'Available');
        CREATE TABLE IF NOT EXISTS pickups(
          id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
          category TEXT NOT NULL, quantity REAL NOT NULL, address TEXT NOT NULL,
          preferred_date TEXT NOT NULL, notes TEXT DEFAULT '',
          status TEXT DEFAULT 'Requested', truck_id INTEGER, driver_id INTEGER,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY(user_id) REFERENCES users(id),
          FOREIGN KEY(truck_id) REFERENCES trucks(id),
          FOREIGN KEY(driver_id) REFERENCES users(id));
        CREATE TABLE IF NOT EXISTS complaints(
          id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
          subject TEXT NOT NULL, message TEXT NOT NULL,
          status TEXT DEFAULT 'Open', created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS recycling(
          id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL,
          quantity REAL NOT NULL, pickup_id INTEGER, recorded_by INTEGER,
          recorded_at TEXT DEFAULT CURRENT_TIMESTAMP);
        """)
        # Demo administrator and driver are created only once.
        if not con.execute("SELECT id FROM users WHERE email='admin@ecotruck.com'").fetchone():
            con.execute("INSERT INTO users(name,email,password,role,phone,address) VALUES(?,?,?,?,?,?)",
                ("EcoTruck Admin","admin@ecotruck.com",generate_password_hash("admin123"),"admin","9000000000","Head Office"))
        if not con.execute("SELECT id FROM users WHERE email='driver@ecotruck.com'").fetchone():
            con.execute("INSERT INTO users(name,email,password,role,phone,address) VALUES(?,?,?,?,?,?)",
                ("Demo Driver","driver@ecotruck.com",generate_password_hash("driver123"),"driver","9000000001","Madurai"))
        if not con.execute("SELECT id FROM trucks").fetchone():
            con.executemany("INSERT INTO trucks(plate,model,capacity,status) VALUES(?,?,?,?)", [
                ("TN-58-EC-1001","Mini Collection Truck",1200,"Available"),
                ("TN-58-EC-1002","Recycling Truck",1800,"Available"),
                ("TN-58-EC-1003","Heavy Waste Truck",2500,"Maintenance")])

init_db()

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapped

def roles(*allowed):
    def decorator(f):
        @wraps(f)
        @login_required
        def wrapped(*args, **kwargs):
            if session.get("role") not in allowed:
                flash("You do not have permission to access that page.", "danger")
                return redirect(url_for("dashboard"))
            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.context_processor
def shared():
    return {"current_user": session, "categories": CATEGORIES}

@app.route("/")
def home():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return render_template("home.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name=request.form.get("name","").strip()
        email=request.form.get("email","").strip().lower()
        password=request.form.get("password","")
        phone=request.form.get("phone","").strip()
        address=request.form.get("address","").strip()
        if not all([name,email,password,address]):
            flash("Please complete all required fields.", "danger")
        elif len(password)<6:
            flash("Password must contain at least 6 characters.", "danger")
        else:
            try:
                with db() as con:
                    con.execute("INSERT INTO users(name,email,password,role,phone,address) VALUES(?,?,?,?,?,?)",
                        (name,email,generate_password_hash(password),"citizen",phone,address))
                flash("Account created. You can now log in.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("That email address is already registered.", "danger")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email","").strip().lower()
        password=request.form.get("password","")
        with db() as con:
            user=con.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone()
        if user and check_password_hash(user["password"],password):
            session.clear()
            session.update(user_id=user["id"],name=user["name"],role=user["role"],email=user["email"])
            flash("Welcome back, "+user["name"]+"!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    with db() as con:
        if session["role"]=="citizen":
            pickups=con.execute("SELECT * FROM pickups WHERE user_id=? ORDER BY id DESC LIMIT 5",(session["user_id"],)).fetchall()
            stats={
                "total":con.execute("SELECT COUNT(*) FROM pickups WHERE user_id=?",(session["user_id"],)).fetchone()[0],
                "completed":con.execute("SELECT COUNT(*) FROM pickups WHERE user_id=? AND status='Completed'",(session["user_id"],)).fetchone()[0],
                "pending":con.execute("SELECT COUNT(*) FROM pickups WHERE user_id=? AND status NOT IN ('Completed','Cancelled')",(session["user_id"],)).fetchone()[0],
                "complaints":con.execute("SELECT COUNT(*) FROM complaints WHERE user_id=?",(session["user_id"],)).fetchone()[0]}
        elif session["role"]=="driver":
            pickups=con.execute("""SELECT p.*,u.name AS citizen FROM pickups p JOIN users u ON p.user_id=u.id
                WHERE p.driver_id=? ORDER BY p.id DESC LIMIT 8""",(session["user_id"],)).fetchall()
            stats={"total":con.execute("SELECT COUNT(*) FROM pickups WHERE driver_id=?",(session["user_id"],)).fetchone()[0],
                   "completed":con.execute("SELECT COUNT(*) FROM pickups WHERE driver_id=? AND status='Completed'",(session["user_id"],)).fetchone()[0],
                   "pending":con.execute("SELECT COUNT(*) FROM pickups WHERE driver_id=? AND status NOT IN ('Completed','Cancelled')",(session["user_id"],)).fetchone()[0],
                   "complaints":0}
        else:
            pickups=con.execute("""SELECT p.*,u.name AS citizen FROM pickups p JOIN users u ON p.user_id=u.id
                ORDER BY p.id DESC LIMIT 8""").fetchall()
            stats={"total":con.execute("SELECT COUNT(*) FROM pickups").fetchone()[0],
                   "completed":con.execute("SELECT COUNT(*) FROM pickups WHERE status='Completed'").fetchone()[0],
                   "pending":con.execute("SELECT COUNT(*) FROM pickups WHERE status NOT IN ('Completed','Cancelled')").fetchone()[0],
                   "complaints":con.execute("SELECT COUNT(*) FROM complaints WHERE status='Open'").fetchone()[0]}
        waste=con.execute("SELECT category,COALESCE(SUM(quantity),0) AS total FROM recycling GROUP BY category ORDER BY total DESC").fetchall()
        truck_count=con.execute("SELECT COUNT(*) FROM trucks").fetchone()[0]
    return render_template("dashboard.html",stats=stats,pickups=pickups,waste=waste,truck_count=truck_count)

@app.route("/pickups")
@login_required
def pickups():
    with db() as con:
        if session["role"]=="citizen":
            rows=con.execute("SELECT p.*,u.name AS citizen,t.plate,d.name AS driver FROM pickups p JOIN users u ON p.user_id=u.id LEFT JOIN trucks t ON p.truck_id=t.id LEFT JOIN users d ON p.driver_id=d.id WHERE p.user_id=? ORDER BY p.id DESC",(session["user_id"],)).fetchall()
        elif session["role"]=="driver":
            rows=con.execute("SELECT p.*,u.name AS citizen,t.plate,d.name AS driver FROM pickups p JOIN users u ON p.user_id=u.id LEFT JOIN trucks t ON p.truck_id=t.id LEFT JOIN users d ON p.driver_id=d.id WHERE p.driver_id=? ORDER BY p.id DESC",(session["user_id"],)).fetchall()
        else:
            rows=con.execute("SELECT p.*,u.name AS citizen,t.plate,d.name AS driver FROM pickups p JOIN users u ON p.user_id=u.id LEFT JOIN trucks t ON p.truck_id=t.id LEFT JOIN users d ON p.driver_id=d.id ORDER BY p.id DESC").fetchall()
        drivers_list=con.execute("SELECT id,name FROM users WHERE role='driver' ORDER BY name").fetchall() if session["role"]=="admin" else []
        trucks_list=con.execute("SELECT id,plate FROM trucks WHERE status='Available' ORDER BY plate").fetchall() if session["role"]=="admin" else []
    return render_template("pickups.html",rows=rows,drivers_list=drivers_list,trucks_list=trucks_list)

@app.route("/pickup/new", methods=["GET","POST"])
@roles("citizen")
def new_pickup():
    if request.method=="POST":
        category=request.form.get("category")
        quantity=request.form.get("quantity","0")
        address=request.form.get("address","").strip()
        date=request.form.get("preferred_date")
        notes=request.form.get("notes","").strip()
        try:
            qty=float(quantity)
            if category not in CATEGORIES or qty<=0 or not address or not date:
                raise ValueError()
            with db() as con:
                con.execute("INSERT INTO pickups(user_id,category,quantity,address,preferred_date,notes) VALUES(?,?,?,?,?,?)",
                    (session["user_id"],category,qty,address,date,notes))
            flash("Pickup request submitted successfully.", "success")
            return redirect(url_for("pickups"))
        except ValueError:
            flash("Enter a valid category, quantity, address and date.", "danger")
    return render_template("new_pickup.html")

@app.route("/pickup/<int:pickup_id>/assign", methods=["POST"])
@roles("admin")
def assign_pickup(pickup_id):
    driver_id=request.form.get("driver_id")
    truck_id=request.form.get("truck_id")
    with db() as con:
        driver=con.execute("SELECT id FROM users WHERE id=? AND role='driver'",(driver_id,)).fetchone()
        truck=con.execute("SELECT id FROM trucks WHERE id=?",(truck_id,)).fetchone()
        if driver and truck:
            con.execute("UPDATE pickups SET driver_id=?,truck_id=?,status='Assigned' WHERE id=?",(driver_id,truck_id,pickup_id))
            flash("Driver and truck assigned.", "success")
        else: flash("Select a valid driver and truck.", "danger")
    return redirect(url_for("pickups"))

@app.route("/pickup/<int:pickup_id>/status", methods=["POST"])
@roles("admin","driver")
def update_status(pickup_id):
    status=request.form.get("status")
    allowed=["Assigned","Picked Up","Completed","Cancelled"]
    with db() as con:
        row=con.execute("SELECT * FROM pickups WHERE id=?",(pickup_id,)).fetchone()
        permitted = session["role"]=="admin" or (row and row["driver_id"]==session["user_id"])
        if row and permitted and status in allowed:
            con.execute("UPDATE pickups SET status=? WHERE id=?",(status,pickup_id))
            if status=="Completed":
                con.execute("INSERT INTO recycling(category,quantity,pickup_id,recorded_by) VALUES(?,?,?,?)",
                    (row["category"],row["quantity"],pickup_id,session["user_id"]))
            flash("Pickup status updated.", "success")
        else: flash("Unable to update this pickup.", "danger")
    return redirect(url_for("pickups"))

@app.route("/trucks", methods=["GET","POST"])
@roles("admin")
def trucks():
    with db() as con:
        if request.method=="POST":
            plate=request.form.get("plate","").strip().upper()
            model=request.form.get("model","").strip()
            try:
                capacity=float(request.form.get("capacity","0"))
                if not plate or not model or capacity<=0: raise ValueError()
                con.execute("INSERT INTO trucks(plate,model,capacity) VALUES(?,?,?)",(plate,model,capacity))
                flash("Truck added successfully.", "success")
                return redirect(url_for("trucks"))
            except ValueError:
                flash("Enter valid truck details. Registration numbers must be unique.", "danger")
            except sqlite3.IntegrityError:
                flash("That registration number already exists.", "danger")
        rows=con.execute("SELECT * FROM trucks ORDER BY id DESC").fetchall()
    return render_template("trucks.html",rows=rows)

@app.route("/drivers")
@roles("admin")
def drivers():
    with db() as con:
        rows=con.execute("SELECT u.*,COUNT(p.id) AS jobs FROM users u LEFT JOIN pickups p ON p.driver_id=u.id WHERE u.role='driver' GROUP BY u.id").fetchall()
    return render_template("drivers.html",rows=rows)

@app.route("/complaints", methods=["GET","POST"])
@login_required
def complaints():
    with db() as con:
        if request.method=="POST" and session["role"]=="citizen":
            subject=request.form.get("subject","").strip()
            message=request.form.get("message","").strip()
            if subject and message:
                con.execute("INSERT INTO complaints(user_id,subject,message) VALUES(?,?,?)",(session["user_id"],subject,message))
                flash("Complaint submitted.", "success")
                return redirect(url_for("complaints"))
            flash("Please enter a subject and message.", "danger")
        if session["role"]=="citizen":
            rows=con.execute("SELECT c.*,u.name FROM complaints c JOIN users u ON u.id=c.user_id WHERE c.user_id=? ORDER BY c.id DESC",(session["user_id"],)).fetchall()
        else:
            rows=con.execute("SELECT c.*,u.name FROM complaints c JOIN users u ON u.id=c.user_id ORDER BY c.id DESC").fetchall()
    return render_template("complaints.html",rows=rows)

@app.route("/complaint/<int:cid>/resolve", methods=["POST"])
@roles("admin")
def resolve_complaint(cid):
    with db() as con:
        con.execute("UPDATE complaints SET status='Resolved' WHERE id=?",(cid,))
    flash("Complaint marked as resolved.", "success")
    return redirect(url_for("complaints"))

@app.route("/reports")
@roles("admin")
def reports():
    with db() as con:
        totals=con.execute("SELECT category,SUM(quantity) AS quantity,COUNT(*) AS jobs FROM recycling GROUP BY category ORDER BY quantity DESC").fetchall()
        statuses=con.execute("SELECT status,COUNT(*) AS count FROM pickups GROUP BY status").fetchall()
        overall=con.execute("SELECT COALESCE(SUM(quantity),0) FROM recycling").fetchone()[0]
        users=con.execute("SELECT COUNT(*) FROM users WHERE role='citizen'").fetchone()[0]
    return render_template("reports.html",totals=totals,statuses=statuses,overall=overall,users=users)

@app.route("/profile", methods=["GET","POST"])
@login_required
def profile():
    with db() as con:
        if request.method=="POST":
            name=request.form.get("name","").strip()
            phone=request.form.get("phone","").strip()
            address=request.form.get("address","").strip()
            if name and address:
                con.execute("UPDATE users SET name=?,phone=?,address=? WHERE id=?",(name,phone,address,session["user_id"]))
                session["name"]=name
                flash("Profile updated.", "success")
                return redirect(url_for("profile"))
        user=con.execute("SELECT * FROM users WHERE id=?",(session["user_id"],)).fetchone()
    return render_template("profile.html",user=user)

if __name__ == "__main__":
    app.run(debug=True)
