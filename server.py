from flask import Flask, render_template, redirect, request
# import the function that will return an instance of a connection
from mysql import connectToMySQL
app = Flask(__name__)


@app.route("/users")
def index():
    mysql = connectToMySQL('users')
    users = mysql.query_db('SELECT * FROM users;')
    return render_template("index.html", all_users=users)


@app.route('/users/new')
def new_user_page():
    return render_template("adduser.html")


@app.route("/add_user", methods=["POST"])
def add_user():
    mysql = connectToMySQL('users')
    query = "INSERT INTO users (FirstName, LastName, Email, description, created_at, updated_at) VALUES (%(firstname)s, %(lastname)s, %(email)s, %(description)s, NOW(), NOW());"
    data = {
        "firstname": request.form["firstname"],
        "lastname": request.form["lastname"],
        "email": request.form["email"],
        "description": request.form["description"]
    }
    id = mysql.query_db(query, data)
    return redirect("/users/" +str(id))


@app.route("/users/<id>/edit")
def edit_user(id):
    mysql = connectToMySQL('users')
    query = 'SELECT * FROM users where id = %(id)s;'
    data = {
        "id": id
    }
    user = mysql.query_db(query, data)
    return render_template("edit.html", id = id, user = user)

@app.route("/updateuser", methods=['POST'])
def update_user():
    mysql = connectToMySQL('users')
    query = "UPDATE users set FirstName = %(firstname)s, LastName = %(lastname)s, Email = %(email)s, description = %(description)s, updated_at = NOW() where id = %(id)s;"
    data = {
        "firstname": request.form["firstname"],
        "lastname": request.form["lastname"],
        "email": request.form["email"],
        "description": request.form["description"],
        "id": request.form["id"]
    }
    mysql.query_db(query,data)
    return redirect("/users/"+ str(request.form['id']))

@app.route("/users/<id>/delete")
def delete_user(id):
    mysql = connectToMySQL('users')
    query = "DELETE from users where id = %(id)s;"
    data = {
        "id": id
    }
    mysql.query_db(query,data)
    return redirect("/users")

@app.route("/users/<id>")
def show_user(id):
    mysql = connectToMySQL('users')
    query = 'SELECT * FROM users where id = %(id)s;'
    data = {
        "id": id
    }
    user = mysql.query_db(query,data)
    return render_template("show_user.html", user = user, id = id)

if __name__ == "__main__":
    app.run(debug=True)
