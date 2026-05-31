
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.secret_key = "plannerkey123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================
# USER MODEL
# ======================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# ======================
# TASK MODEL
# ======================
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    due = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

# ======================
# HOME (TEST FIRST)
# ======================
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    tasks = Task.query.filter_by(user_id=session["user_id"]).all()
    return render_template("dashboard.html", tasks=tasks)

# ======================
# REGISTER
# ======================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"]
        )

        if User.query.filter_by(username=user.username).first():
            return "User exists"

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# ======================
# LOGIN
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect("/")
        return "Invalid login"

    return render_template("login.html")

# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ======================
# ADD TASK
# ======================
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        task = Task(
            title=request.form["title"],
            due=request.form["due"],
            priority=request.form["priority"],
            user_id=session["user_id"]
        )
        db.session.add(task)
        db.session.commit()
        return redirect("/")

    return render_template("add_task.html")

# ======================
# COMPLETE TASK
# ======================
@app.route("/complete/<int:id>")
def complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect("/")

# ======================
# DELETE TASK
# ======================
@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

# ======================
# EDIT TASK
# ======================
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task = Task.query.get_or_404(id)

    if request.method == "POST":
        task.title = request.form["title"]
        task.due = request.form["due"]
        task.priority = request.form["priority"]
        db.session.commit()
        return redirect("/")

    return render_template("edit_task.html", task=task)
    return "DEPLOY WORKING SUCCESSFULLY"

if __name__ == "__main__":
    app.run(debug=True)
    app.run()
