from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db_name = "users.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{db}'.format(db=db_name)
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

app.config['SECRET_KEY'] = 'au33UqFOJ64LE8iWl8CJyS7NYvwFegwF'

db = SQLAlchemy(app)

def create_test_users():
    test_users = {
        "adam": "abcabc",
        "bart": "testtest",
        "jack": "hello"
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

    def __repr__(self):
        return '' % self.username

# user registration
@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # get the data from HTML form
        username = request.form['username']
        password = request.form['password']

        # check form data
        if not (username and password):
            flash("Username or Password cannot be empty")
            # redirect back
            return redirect(url_for('register'))
        else:
            username = username.strip()
            password = password.strip()

        # hash the password
        hashed_pwd = generate_password_hash(password, 'sha256')
        #print("dupa")
        # create the User from model and add to database
        new_user = User(username=username, pass_hash=hashed_pwd)
        db.session.add(new_user)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash(f"Username {username} is not available.")
            return redirect(url_for('register'))

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
        if user and check_password_hash(user.pass_hash, password):
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

    return render_template("user_home.html", username=username)

# logout current user
@app.route("/logout/<username>")
def logout(username):
    # delete the session cookie
    session.pop(username, None)
    flash("sucessfully logged out.")
    # redirect back to login page
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)