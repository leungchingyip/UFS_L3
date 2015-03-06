
from flask import Flask, session, render_template, redirect, url_for, request, jsonify

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from model import Base, Category, Item


from hashlib import sha256

import jinja2 

import string, random

from flask_wtf.csrf import CsrfProtect

from datetime import datetime

app = Flask(__name__)

# Run Flask_WTF's CRSFProtect
CsrfProtect(app)
WTF_CSRF_SECRET_KEY = "uuuuuuuuuuuuuuu"

# Login Username and Password.
username = "a"
password = "a"

# This secret is used for Flask's session
app.secret_key= "uuuuuuuuuuuuuuu"

# Initialize and connect database by SQLAlchemy
engine = create_engine('postgresql://django:mimetext@localhost/catalog')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



# Faked database for test
# c = [{'name': 'Basketball'}, 
# {'name':'Football'},
# {'name':'Surf'}]

# items = [{'name': 'Kobe 8', 'discription':'Shoe', 'photo':'http://www.csneaker.com/wp-content/uploads/2012/05/30/NIKE-ZOOM-KOBE-VII-SYSTEM-Mens-Basketball-Shoe1.jpg', 'category':'Basketball'},
# 		{'name': 'GN10', 'discription':'Shoe', 'photo':'http://6.kicksonfire.net/wp-content/uploads/2009/06/nikefpii1.jpg', 'category':'Basketball'},
# 		{'name': 'C9', 'discription':'Boot', 'photo':'http://theoriginalwinger.com/wp-content/uploads/2013/03/nike-cristiano-ronaldo-nike-summer-collection-boots.jpg', 'category':'Football'},
# 		{'name': 'Messi', 'discription':'Boot', 'photo':'http://3.bp.blogspot.com/-ZGOPmWts0ds/UMZG9YGdrMI/AAAAAAAADDc/wpAEHuFA-Qc/w800/Adidas%2BAdiZero%2BIII%2B2013%2BMessi%2BBoots.jpg', 'category':'Football'}
# ]

# i = {'name': 'Messi', 'discription':'Boot', 'photo':'http://3.bp.blogspot.com/-ZGOPmWts0ds/UMZG9YGdrMI/AAAAAAAADDc/wpAEHuFA-Qc/w800/Adidas%2BAdiZero%2BIII%2B2013%2BMessi%2BBoots.jpg', 'category':'Football'}


# Initialize template environment
env = jinja2.Environment(loader=jinja2.PackageLoader('catalog', 'templates'))

# This function make ramdom string for???
def string_generator(size=30, chars=string.ascii_letters):
	return ''.join(random.choice(chars) for _ in range(size))

# This secret is used for function make_cookie()
cookie_secret = "udacityisawesome"

# Hash username and cookies, return the username and a hash string
def make_cookie(name):
	return "%s|%s"%(name, sha256(name+cookie_secret).hexdigest())

# Set cookies
def set_user_cookie(name, obj):
	cookie = make_cookie(name)
	obj.set_cookie("name", value=cookie)

# Check cookie, if cookies valid, return username, else return False
def check_cookie():
	if request.cookies.get("name"):
		cookie = request.cookies.get("name")
		c = cookie.split("|")
		if sha256(c[0]+cookie_secret).hexdigest() == c[1]:
			return c[0]
		else:
			return False
	else:
		return False

# Login, redirect to homepage, set cookie if username and password is vaild
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method=='POST':
		if request.form['username'] == username and request.form['password'] == password:
			response = redirect("/")
			set_user_cookie(username, response)
			return response
		else: 
			return redirect("/")
	else:
		return redirect("/")

# Logout, redirect to homepage 
@app.route('/logout', methods=['GET', 'POST'])
def logout():
	response = redirect("/")
	#set the clear the cookie[name]
	response.set_cookie('name', '')
	return response



@app.route('/', methods=['GET', 'POST'])
def showAll():
	'''This page will show all items, order by adding time'''
	login_already = check_cookie()
	i = session.query(Item).order_by(desc(Item.create_time)).all()
	c = session.query(Category).all()
	return render_template("home.html", c=c, items=i, login_already=login_already)

@app.route('/add', methods=['GET', 'POST'])
def newItem():
	'''This page will be for adding a new item'''
	login_already=check_cookie()
	# This function will return to homepage if it found user is not login. There are several similar setting in the function below which are able to edit the database. 
	if login_already:
		if request.method == "POST":
			# Get currunt time and insert to create_time. This will use for index items display order
			time_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			i = Item(create_time=time_now, 
				id=request.form['name'],
				name=request.form['name'], 
				discription=request.form['discription'], 
				photo=request.form['photo'], 
				category=request.form['category'])
			session.add(i)
			session.commit()
			return redirect("/")
		c = session.query(Category).all()
		return render_template("add.html", c=c, login_already=login_already)
	else:
		return redirect("/")

@app.route('/catalog/<category>/items', methods=['GET', 'POST'])
def showcategoryItem(category):
	'''This page will be for showing all items in the category'''
	login_already=check_cookie()
	# Get all items in the selected category 
	i = session.query(Item).filter_by(category=category).order_by(desc(Item.create_time)).all()
	c = session.query(Category).all()
	return render_template("home.html", c=c, items=i, login_already=login_already)

@app.route('/item/<item>', methods=['GET', 'POST'])
def showItem(item):
	'''This page will be for showing the selected item'''
	login_already=check_cookie()
	i = session.query(Item).filter_by(id=item).one()
	c = session.query(Category).all()
	return render_template("item.html", c=c, item=i, login_already=login_already)

@app.route('/<item>/edit', methods=['GET', 'POST'])
def editItem(item):
	'''This page will be for editing the selected item'''
	login_already=check_cookie()
	if login_already:
		i = session.query(Item).filter_by(id=item).one()
		if request.method == "POST":
			# Update the infomation of the item. Item's id is use for index the url, so it will not change. Ids of items will always be the name that created at first time.
			i.name= request.form['name']
			i.discription= request.form['discription']
			i.photo= request.form['photo']
			i.category= request.form['category']
			session.add(i)
			session.commit()
			return redirect("/item/%s" %item)
		i=session.query(Item).filter_by(id=item).one()
		c=session.query(Category).all()
		return render_template("edit.html", c=c, item=i, login_already=login_already)
	else:
		return redirect("/")

@app.route('/<item>/delete', methods=['GET', 'POST'])
def deleteItem(item):
	'''This page will be for deleting the selected item'''
	login_already=check_cookie()
	if login_already:
		if request.method == "POST":
			# This post request is submited automatically in delete.html for csrf protection.
			if request.form['delete_it'] == "yes":
				i = session.query(Item).filter_by(id=item).one()
				session.delete(i)
				session.commit()
				return redirect("/")
		return render_template("delete.html")
	else:
		return redirect("/")

@app.route('/newcategory', methods=['GET', 'POST'])
def newcategory():
	'''This page will be for create a new category'''
	login_already=check_cookie()
	if login_already:
		if request.method=='POST':
			i = Category(name=request.form['name'])
			session.add(i)
			session.commit()
			return redirect("/")
		c=session.query(Category).all()
		return render_template("newcategory.html", c=c, login_already=login_already)
	else:
		return redirect("/")

# Below is the JSON session 

@app.route('/JSON', methods=['GET', 'POST'])
def categoryItemJSON():
	'''This page will be for showing all items in the category in JSON'''
	c = session.query(Category).all()
	return jsonify(Caregory=[i.serialize for i in c])

@app.route('/item/<item>/JSON', methods=['GET', 'POST'])
def showItemJSON(item):
	'''This page will be for showing the selected item in JSON'''
	i = session.query(Item).filter_by(id=item).one()
	return jsonify(i.serialize)

@app.route('/catalog/<category>/items/JSON', methods=['GET', 'POST'])
def showcategoryItemJSON(category):
	'''This page will be for showing all items in the category in JSON'''
	i = session.query(Item).filter_by(category=category).order_by(desc(Item.create_time)).all()
	return jsonify(Category=[item.serialize for item in i])


# run the app by "python catalog.py". False debug before put it online.
if __name__ == "__main__":
    app.run(debug=True)