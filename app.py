from flask import Flask, render_template, request, redirect, url_for
from models.user import Db, User
from modules.userform import UserForm
from random_word import RandomWords
from random import randint
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/userdb'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "s14a-key"
app.config.update(
    SECRET_KEY = "s14a-key"
)
Db.init_app(app)


r = RandomWords()

@app.route('/')
def index():
    user_list = []
    users = User.query.all()
    for user in users:
        user_list.append(User.toString(user))
    
    return render_template("index.html", userList=user_list)

# @route /adduser - GET, POST
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = UserForm()
    # If GET
    if request.method == 'GET':
        return render_template('adduser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            new_user = User(first_name=first_name, age=age)
            Db.session.add(new_user)
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('adduser.html', form=form)

# @route /adduser/<first_name>/<age>
@app.route('/adduser/<first_name>/<age>')
def addUserFromUrl(first_name, age):
    Db.session.add(User(first_name=first_name, age=age))
    Db.session.commit()
    return redirect(url_for('index'))

def getuser(db_id):
    user = User.query.filter(User.user_id == db_id).all()
    if(len(user) == 0):
        return None
    if(len(user) != 1):
        print(f"WARN: More than one result for id: '{db_id}'")
    return user[0]


@app.route('/finduser/<db_id>')
def finduser(db_id):
    if(db_id is None):
        return "Please add a user id. E.g. <>/finduser/10"
    user = getuser(db_id)
    if(user is None):
        return f"No user found for id: '{db_id}'"
    return User.toString(user);


@app.route('/deleteuser/<db_id>')
def deleteuser(db_id):
    if(db_id is None):
        return "Please add a user id. E.g. <>/deleteuser/10"
    user = getuser(db_id)
    if(user is None):
        return f"No user found for id: '{db_id}'"
    Db.session.delete(user)
    Db.session.commit()
    return "User deleted"

@app.route('/addrandomuser')
def addrandomuser():
    try:
        first, last = r.get_random_word().capitalize(), r.get_random_word().capitalize()
    catch Exception as e:
	print(str(e))
        first, last = "Random", "Name"
    name = " ".join([first, last])
    age = randint(1,100)
    Db.session.add(User(first_name=name, age=age))
    Db.session.commit()
    return redirect(url_for('index'))
    


