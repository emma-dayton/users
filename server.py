from flask import Flask, render_template, request, redirect, session
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'e7ef0a420bb411f5e8222ee7345fab24'


# users route is home -- displays all users in database
@app.route('/users')
def index():
    session['title'] = 'All Users'
    db = connectToMySQL('users_dojo_db')
    users = db.query_db("SELECT * FROM users;")
    print(users)
    return render_template("all_users.html", users=users)


# renders html page with form for adding new user
@app.route('/users/new')
def add():
    session['title'] = 'Add User'
    return render_template("add_user.html")


# adds the new user from the previous route, redirects to main users page
@app.route('/users/create', methods=['POST'])
def add_user():
    db = connectToMySQL('users_dojo_db')
    data = {
    'fn': request.form['fname'],
    'ln': request.form['lname'],
    'email': request.form['email'],
    }
    print(data)
    query = '''INSERT INTO users (first_name, last_name, email,
    created_at, updated_at) VALUES(%(fn)s, %(ln)s, %(email)s, now(), now())'''
    db.query_db(query, data)
    return redirect('/users')


# shows information for an individual user
@app.route('/users/<num>')
def show_user(num):
    num_id = {'n':int(num)}
    db = connectToMySQL('users_dojo_db')
    query = 'SELECT * FROM users WHERE id = %(n)s;'
    user = db.query_db(query, num_id)
    user = user[0]
    print(user)
    session['title'] = f"{user['first_name']} {user['last_name']}"
    return render_template('user.html', user=user)


# renders html for form to update user in database (prepopulated with current info)
@app.route('/users/<num>/edit')
def edit_user(num):
    num_id = {'n':int(num)}
    db = connectToMySQL('users_dojo_db')
    query = 'SELECT * FROM users WHERE id = %(n)s;'
    user = db.query_db(query, num_id)
    user = user[0]
    session['title'] = f"Edit {user['first_name']} {user['last_name']}"
    return render_template('edit_user.html', user=user)


# updates info in database for user, redirects to users home page
@app.route('/users/<num>/update', methods=['POST'])
def edit_user_submit(num):
    db = connectToMySQL('users_dojo_db')
    data = {
    'num_id': int(num),
    'fn': request.form['fname'],
    'ln': request.form['lname'],
    'email': request.form['email'],
    }
    query = '''UPDATE users SET first_name = %(fn)s, last_name = %(ln)s,
            email = %(email)s, updated_at=now() WHERE id=%(num_id)s'''
    db.query_db(query, data)
    return redirect ('/users')


# deletes user from database
@app.route('/users/<num>/destroy')
def destroy(num):
    num_id = {'n':int(num)}
    db = connectToMySQL('users_dojo_db')
    query = 'DELETE FROM users WHERE id = %(n)s'
    db.query_db(query, num_id)
    return redirect('/users')



if __name__ == "__main__":
    app.run(debug=True)
