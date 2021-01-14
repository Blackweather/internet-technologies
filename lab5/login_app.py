from flask import Flask, render_template, request, url_for, redirect, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'au33UqFOJ64LE8iWl8CJyS7NYvwFegwF'

# user login
@app.route("/", methods=["GET", "POST"])
def route_main():
  return render_template("login.html") 

if __name__ == "__main__":
    app.run(port=5000, debug=True)
