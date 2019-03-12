from flask import Flask, render_template, request, redirect, session
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'e7ef0a420bb411f5e8222ee7345fab24'
# our index route will handle rendering our form
@app.route('/')
def index():
    if 'header' not in session:
        session['header'] = 'All Users'
    db = connectToMySQL('users_dojo_db')
    users = db.query_db("SELECT * FROM users;")
    print(users)
    return render_template("all_users.html")
#
#
@app.route('/add_user', methods=['POST'])
def add_user():
    session['header'] = 'Add a New User'
    db = connectToMySQL('users_dojo_db')
    data = {
    'fn': request.form('first_name'),
    'ln': request.form('last_name'),
    'email': request.form('email'),
    }
    print(data)
    query = '''INSERT INTO users_dojo_db (first_name, last_name, email,
    created_at, updated_at) VALUES(%(fn)s, %(ln)s, %(email)s, now(), now())'''
    db.query_db(query, data)
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)
