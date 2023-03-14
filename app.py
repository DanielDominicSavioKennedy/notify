from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config["SECRET_KEY"] = "WebsiteMadeByDom"


# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    phno=db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

# Login Manager

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated, user=current_user)


# User login part
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        name, password, email, phno = request.form.get("name"), request.form.get("password"), request.form.get("email"), request.form.get("phno")

        new_user = User(
            name = name,
            email = email,
            password = password,
            phno=phno
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template("register.html", logged_in=current_user.is_authenticated)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            password = request.form.get("password")
            if user.password == password:
                login_user(user)
                return redirect(url_for("home"))

            flash("Invalid password")
            return redirect(url_for("login"))

        flash("User not registered with email!")
        return redirect(url_for("login"))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
