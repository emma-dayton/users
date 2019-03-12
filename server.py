from flask import Flask, render_template, request, redirect, session
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'e7ef0a420bb411f5e8222ee7345fab24'
# our index route will handle rendering our form
@app.route('/users')
def index():
    session['title'] = 'All Users'
    db = connectToMySQL('users_dojo_db')
    users = db.query_db("SELECT * FROM users;")
    print(users)
    return render_template("all_users.html", users=users)
#
#
@app.route('/users/add')
def add():
    session['title'] = 'Add User'
    return render_template("add_user.html")

@app.route('/users/add/add_user', methods=['POST'])
def add_user():
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
    return redirect('/users')

@app.route('/users/<num>/show')
def show_user(num):
    num = num
    db = connectToMySQL('users_dojo_db')
    query = f'SELECT * FROM users WHERE id = {num} ;'
    user = db.query_db(query)
    user = user[0]
    print(user)
    session['title'] = f"{user['first_name']} {user['last_name']}"
    return render_template('user.html', user=user)


if __name__ == "__main__":
    app.run(debug=True)
