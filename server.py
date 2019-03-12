from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)
# our index route will handle rendering our form
@app.route('/')
def index():
    db = connectToMySQL('users_dojo_db')
    pets = db.query_db("SELECT * FROM pets;")
    print(pets)
    return render_template("index.html", pets=pets)


@app.route('/add_user', methods=['POST'])
def safe_add_pet():
    db = connectToMySQL('users_dojo_db')
    data = {
    }
    print(data)
    query = 'INSERT INTO users_dojo_db (name, species, created_at, updated_at) VALUES(%(?????)s, %(????)s, now(), now())'
    db.query_db(query, data)
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)
