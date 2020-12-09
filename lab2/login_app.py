from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
import smtplib
from hashlib import sha256
import traceback

db_name = "users.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{db}'.format(db=db_name)
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

app.config['SECRET_KEY'] = 'au33UqFOJ64LE8iWl8CJyS7NYvwFegwF'

db = SQLAlchemy(app)


def create_test_users():
    test_users = {
        "adam": "abcabc",
        "filip": "filip",
        "karol": "karol"
    }

    for k in test_users.keys():
        hashed_pwd = generate_password_hash(test_users[k], 'sha256')
        u = User(username=k, pass_hash=hashed_pwd)
        db.session.add(u)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            print(f"Failed to add user {k}.")

        print(f"User account {k} has been created.")



# execute to create a new DB
def create_db():
    db.create_all()
    create_test_users()


# database user model
class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pass_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50))

    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    street = db.Column(db.String(100))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(10))
    age = db.Column(db.Integer)
    pesel = db.Column(db.String(11))
    activation_hash = db.Column(db.String(32))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# user registration
@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # get the data from HTML form
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        street = request.form['street']
        city = request.form['city']
        country = request.form['country']
        postal_code = request.form['postal_code']
        age = request.form['age']
        pesel = request.form['pesel']

        form_correct = True

        # check if form not empty
        if not (
            username and password and 
            email and first_name and 
            last_name and street and 
            city and country and postal_code
            and age and pesel):
                flash("All the values need to be filled in")
                form_correct = False
        else:
            username = username.strip()
            password = password.strip()
            email = email.strip()
            first_name = first_name.strip()
            last_name = last_name.strip()
            street = street.strip()
            city = city.strip()
            country = country.strip()
            postal_code = postal_code.strip()
            age = age.strip()
            pesel = pesel.strip()

        # validations
        post_code_re = re.compile("[0-9]{2}-[0-9]{3}")

        if not first_name.istitle():
            form_correct = False
            flash("First name needs to be capitalized")
        if not last_name.istitle():
            form_correct = False
            flash("Last name needs to be capitalized")
        if not city.istitle():
            form_correct = False
            flash("City needs to be capitalized")
        if not country.istitle():
            form_correct = False
            flash("Country needs to be capitalized")

        if not post_code_re.search(postal_code):
            form_correct = False
            flash("Your postal code is invalid, use the xx-xxx format")

        try:
            if not (10 < int(age) < 124):
                form_correct = False
                flash("Wrong age")
        except ValueError:
            form_correct = False
            flash("Age must be a number")

        if not (len(pesel) == 11):
            form_correct = False
            flash("Wrong PESEL length")

        if not form_correct:
            return redirect(url_for("register"))

        # hash the password
        hashed_pwd = generate_password_hash(password, 'sha256')
        activation_hash = sha256(str(pesel).encode('utf-8')).hexdigest()
        # create the User from model and add to database
        new_user = User(username=username, 
                        pass_hash=hashed_pwd,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        street=street,
                        city=city,
                        country=country,
                        postal_code=postal_code,
                        age=age,
                        pesel=pesel,
                        activation_hash=activation_hash)
        db.session.add(new_user)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash(f"Username {username} is not available.")

        # emacs sendmail
        sender = 'tt2248893@gmail.com'
        receivers = email

        message ="""From: From mysuperwebsite <tt2248893@gmail.com>
        To: Our beautiful user <{0}>
        Subject: SMTP e-mail test

        {1}
        """.format(email,f"{request.host_url[:-1]}{url_for('activate', username=username)}?hash={activation_hash}")

        try:
            smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtpObj.ehlo()
            smtpObj.login(sender, "$tT2248894")
            smtpObj.sendmail(sender, receivers, message)
            smtpObj.quit()
        except smtplib.SMTPException:
            traceback.print_exc()
            print("Unable to send email")

        flash("User account has been created.")
        return redirect(url_for("login"))

    return render_template("register.html")

# user login
@app.route("/", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    # get data from HTML form
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # check form data
        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        user = User.query.filter_by(username=username).first()

        # check if the provided credentials are valid
        if user == None:
            flash("Access denied")
        elif user.activation_hash != None and user.activation_hash != "":
            flash("Your account is not activated yet")
        elif check_password_hash(user.pass_hash, password):
            session[username] = True
            return redirect(url_for('user_home', username=username))
        else:
            flash("Access denied")

    return render_template("login.html")

# logged in user homepage
@app.route("/user/<username>")
def user_home(username):
    # check if the session cookie is valid
    if not session.get(username):
        abort(401)

    user = User.query.filter_by(username=username).first()
    hidden = ["pass_hash", "uid", "activation_hash", "username"]
    translator = {
        "email": "Email",
        "first_name": "First name",
        "last_name": "Last name",
        "street": "Street",
        "city": "City",
        "country": "Country",
        "postal_code": "Postal code",
        "age": "Age",
        "pesel": "PESEL"
    }

    return render_template("user_home.html", username=username, user=user, 
        hidden=hidden, tr=translator)

# logout current user
@app.route("/logout/<username>")
def logout(username):
    # delete the session cookie
    session.pop(username, None)
    flash("successfully logged out.")
    # redirect back to login page
    return redirect(url_for('login'))

@app.route("/user/activate/<username>")
def activate(username):
    user = User.query.filter_by(username=username).first()
    activation_hash = request.args.to_dict()['hash']

    if user and user.activation_hash == activation_hash:
        user.activation_hash = ""
        db.session.commit()

        flash("User activated!")
    else:
        flash("Did not activate")

    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
