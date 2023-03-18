from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, date
import datetime as dt
from twilio.rest import Client

app = Flask(__name__)

app.config["SECRET_KEY"] = "WebsiteMadeByDom"

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    phno=db.Column(db.Text, nullable=False)
    datelist= db.Column(db.Text, nullable=False)
    pdate = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

#Twillo
account_sid = 'AC99d7765d763b3d0eddb60b19a0f62d27'
auth_token = '6283be6e913eb4223ac51f3eb7b5dbb6'
client = Client(account_sid, auth_token)
def sendMessage(name,phno):
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body="Hey {}!\nYour periods are on the way\n\nItems you might need:\n\nhttps://www.bigbasket.com/pc/beauty-hygiene/feminine-hygiene/tampons-menstrual-cups/\n\nhttps://www.stayfree.in/products\n\nhttps://www.bigbasket.com/ps/?q=period%20heat%20pack&nc=pscs#!page=1".format(name),
    to="whatsapp:+91{}".format(phno)
    )
    print("message sent")
#sendMessage("dominic",6305461499)


def daysCal(datelist):
    datelist = [datetime.strptime(d, '%Y-%m-%d') for d in datelist]
    # calculate the total number of days between all dates
    num_days = list()
    for i in range(len(datelist) - 1):
        delta = datelist[i+1] - datelist[i]
        num_days.append(str(delta).split(" ")[0])
    return num_days

def calPdate(datelist):
    datelist = [datetime.strptime(d, '%Y-%m-%d') for d in datelist]
    # calculate the total number of days between all dates
    num_days = 0
    for i in range(len(datelist) - 1):
        delta = datelist[i+1] - datelist[i]
        num_days += delta.days
    # calculate the average number of days between all dates
    avg_days = num_days / (len(datelist) - 1)
    # define the starting date
    start_date = datelist[-1]
    # calculate the ending date
    end_date = start_date + timedelta(days=avg_days)
    end_date=str(end_date).split(" ")[0]
    #print("Predicted date = ",end_date) # output: 2023-03-22 00:00:00
    return end_date


#Scheduler
def action():
    print("Scheduler is working")
    with app.app_context():
        results = User.query.filter_by(pdate=str(dt.date.today())).all()
    for result in results:
        sendMessage(result.name,result.phno)
    print("Sent")

"""def test():
    #app.app_context().push()
    with app.app_context():
        results = User.query.filter_by(name="asd").all()
    a=list()
    for i in results:
        a.append(i.name)
    print(a)
    return a"""

scheduler = BackgroundScheduler()
scheduler.add_job(action, 'interval', seconds=5)
scheduler.start()

@app.route("/")
def home():
    return render_template("home.html", logged_in=current_user.is_authenticated, user=current_user)


# User login part
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":       
        name, password, email, phno, datelist= request.form.get("name"), request.form.get("password"), request.form.get("email"), request.form.get("phno"),  request.form.get("datelist")
        new_user = User(
            name = name,
            email = email,
            password = password,
            phno=phno,
            datelist=datelist,
            pdate=calPdate(datelist.split(","))
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
        return redirect(url_for("register"))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/update",methods=['GET','POST'])
@login_required
def update():
    print("check1")
    user=current_user
    li=user.datelist.split(",")
    li.append(request.form.get("date"))
    user.datelist=str(",".join(li))
    user.pdate =calPdate(li)
    db.session.commit()
    return redirect(url_for("check"))


@app.route("/check")
@login_required
def check():
    return render_template("check.html",user=current_user,datelist=current_user.datelist.split(",")[1:],nodays=daysCal(current_user.datelist.split(",")))


if __name__ == "__main__":
    app.run(debug=False)