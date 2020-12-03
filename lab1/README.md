# Lab 1 - simple user login and registration
## Running the application
1. Install python packages, run:
```
$ pip install -r requirements.txt
```

2. Initialize the SQLite database
```
$ python
>>> from login_app import create_db
>>> create_db()
>>> exit()
```

3. Run the application
```
$ python login_app.py
```

The application is accessible at http://localhost:5000