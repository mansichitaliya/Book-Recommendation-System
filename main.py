import flask
from flask import Flask, render_template, request, redirect, url_for, session
from RatingBased import *
from content_based_filtering import *
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import flash
import re
import re
import os
from flask_mail import Mail, Message
from book_recommendation import *



app = Flask(__name__)

#for DB
app.secret_key = str(os.urandom(24))
app.config['MYSQL_HOST'] = 'sql5.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql5668611'
app.config['MYSQL_PASSWORD'] = 'QdUpXDQcmp'
app.config['MYSQL_DB'] = 'sql5668611'
mysql = MySQL(app)

#end DB

try:
    if mysql.connection is not None:
        mysql.connection.ping(reconnect=True)
        print("MySQL connection established successfully!")
    else:
        raise Exception("MySQL connection is None.")
except Exception as e:
    print("Error connecting to MySQL:", e)
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bhosaleprithv96@gmail.com'
app.config['MAIL_PASSWORD'] = 'password@saurabhmishra.mylibrary'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



@app.route('/')
def index():
	data = RatingBasedRecommendation()
	nameB, urlB, ratingB = topingenre('Business')
	nameF, urlF, ratingF = topingenre('Non-Fiction')
	nameT, urlT, ratingT = topratedcontent()
	nameA1, urlA1, ratingA1 = randombooks()
	nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
	return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)

#@app.route('/index.html')
#def index():
#	data = RatingBasedRecommendation()
#	#print(data)
#	return render_template('index.html', result = data)

@app.route('/404.html')
def notfound():
	#data = RatingBasedRecommendation()
	#print(data)
	return render_template('404.html')

@app.route('/contentbasedb', methods=['GET', 'POST'])
def contentbasedb():
        #        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
	#result={}
	#result['name']=m_name
	m_name = request.args.get('name')
	#print(m_name)
	m_name, genre = findgenre(m_name)
	#print(m_name, genre)
	name, url, author, rating, genre, Desc = recommenddesc(m_name, genre)
	return (flask.render_template('movielist2.html',target=m_name, name=name, url=url, author=author, rating=rating, genre=genre, Desc=Desc))


@app.route('/userbased.html', methods=['GET', 'POST'])
def userbasedrec():
        #        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
	#result={}
	#result['name']=m_name
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM userdata WHERE id = % s', (session['id'], ))
		account = cursor.fetchone()
		rbook=UserBasedCF(account['id'])
		return render_template('movielist3.html', account = account, rbook=rbook)
	data = RatingBasedRecommendation()
	nameB, urlB, ratingB = topingenre('Business')
	nameF, urlF, ratingF = topingenre('Non-Fiction')
	nameT, urlT, ratingT = topratedcontent()
	nameA1, urlA1, ratingA1 = randombooks()
	nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
	return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)

	# m_name = request.args.get('name')
	# #print(m_name)
	# m_name, genre = findgenre(m_name)
	# #print(m_name, genre)
	# name, url, author, rating, genre, Desc = recommenddesc(m_name, genre)
	# return (flask.render_template('movielist3.html',target=m_name, name=name, url=url, author=author, rating=rating, genre=genre, Desc=Desc))

@app.route('/itembased.html', methods=['GET', 'POST'])
def itembasedrec():
        #        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
	#result={}
	#result['name']=m_name
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM userdata WHERE id = % s', (session['id'], ))
		account = cursor.fetchone()
		rbook=ItemBasedCF(account['id'])
		return render_template('movielist3.html', account = account, rbook=rbook)
	data = RatingBasedRecommendation()
	nameB, urlB, ratingB = topingenre('Business')
	nameF, urlF, ratingF = topingenre('Non-Fiction')
	nameT, urlT, ratingT = topratedcontent()
	nameA1, urlA1, ratingA1 = randombooks()
	nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
	return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)


@app.route('/rateitem', methods=['GET', 'POST'])
def rateitem():
        #        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
	#result={}
	#result['name']=m_name
	ISBN = request.args.get('name')
	#print(m_name)
	
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM userdata WHERE id = % s', (session['id'], ))
		account = cursor.fetchone()
		rbook=searchandrate(ISBN) 
		return render_template('userrate.html', account = account, rbook=rbook)   
	data = RatingBasedRecommendation()
	nameB, urlB, ratingB = topingenre('Business')
	nameF, urlF, ratingF = topingenre('Non-Fiction')
	nameT, urlT, ratingT = topratedcontent()
	nameA1, urlA1, ratingA1 = randombooks()
	nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
	return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)

	# #print(m_name, genre)
	# name, url, author, rating, genre, Desc = recommenddesc(m_name, genre)
	# return (flask.render_template('movielist2.html',target=m_name, name=name, url=url, author=author, rating=rating, genre=genre, Desc=Desc))



@app.route('/search.html', methods=['GET', 'POST'])
def search():
	if flask.request.method == 'GET':
		data = RatingBasedRecommendation()
		nameB, urlB, ratingB = topingenre('Business')
		nameF, urlF, ratingF = topingenre('Non-Fiction')
		nameT, urlT, ratingT = topratedcontent()
		nameA1, urlA1, ratingA1 = randombooks()
		nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
		return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)

	if flask.request.method == 'POST':
		m_name = flask.request.form['book_name']
		m_name = m_name.title()
        #        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
		if(checkavailable(str(m_name))==False):
			result={}
			result['name'] = m_name
			return (flask.render_template('404.html', result=result))
		else:
			result={}
			result['name']=m_name
			m_name, genre = findgenre(m_name)
			name, url, author, rating, genre, Desc = recommenddesc(m_name, genre)
			return (flask.render_template('movielist.html',target=m_name, name=name, url=url, author=author, rating=rating, genre=genre, Desc=Desc))

@app.route('/homev2.html')
def rating():
	data = RatingBasedRecommendation()
	nameB, urlB, ratingB = topingenre('Business')
	nameF, urlF, ratingF = topingenre('Non-Fiction')
	nameT, urlT, ratingT = topratedcontent()
	nameA1, urlA1, ratingA1 = randombooks()
	nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
	return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)

@app.route('/ratebook.html', methods=['GET', 'POST'])
def ratebook():
        #        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
	#result={}
	#result['name']=m_name
	#m_name = request.args.get('name')
	#print(m_name)
	#m_name, genre = findgenre(m_name)
	#print(m_name, genre)
	#name, url, author, rating, genre, Desc = recommenddesc(m_name, genre)
	##data = RatingBasedRecommendation()
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM userdata WHERE id = % s', (session['id'], ))
		account = cursor.fetchone()
		rbook=getrandombooks() 
		return render_template('userrate.html', account = account, rbook=rbook)   
	data = RatingBasedRecommendation()
	nameB, urlB, ratingB = topingenre('Business')
	nameF, urlF, ratingF = topingenre('Non-Fiction')
	nameT, urlT, ratingT = topratedcontent()
	nameA1, urlA1, ratingA1 = randombooks()
	nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
	return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)

@app.route('/ratebook2.html', methods=['GET', 'POST'])
def ratebook2():
        #        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
	#result={}
	#result['name']=m_name
	#m_name = request.args.get('name')
	#print(m_name)
	#m_name, genre = findgenre(m_name)
	#print(m_name, genre)
	#name, url, author, rating, genre, Desc = recommenddesc(m_name, genre)
	##data = RatingBasedRecommendation()
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM userdata WHERE id = % s', (session['id'], ))
		account = cursor.fetchone()
		rbook=getrandombooks()
		if request.method == 'POST' and 'ISBN' in request.form and 'rating' in request.form:
			ISBN = request.form['ISBN']
			#print(ISBN)
			rating = request.form['rating']
			#print(rating)
			#print(account['id'])
			cursor.execute('INSERT INTO userratings VALUES (NULL, % s, % s, % s)', (account['id'], ISBN, rating,))
			mysql.connection.commit()
			#return render_template('<h1>Done</h1>')
		return render_template('userrate.html', account = account, rbook=rbook)   
	data = RatingBasedRecommendation()
	nameB, urlB, ratingB = topingenre('Business')
	nameF, urlF, ratingF = topingenre('Non-Fiction')
	nameT, urlT, ratingT = topratedcontent()
	nameA1, urlA1, ratingA1 = randombooks()
	nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
	return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)
	


@app.route('/register.html', methods=['GET', 'POST'])
def register():
	msg = ''
	regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'password2' in request.form and 'email' in request.form and 'location' in request.form and 'age' in request.form:
		username = request.form['username']
		password = request.form['password']
		repassword = request.form['password2']
		location = request.form['location']
		age = request.form['age']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM userdata WHERE email = % s', (email, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists!'
			return render_template('message.html', msg=msg)
		if(not re.search(regex, email)):
			msg="Invalid Email ID, An email is a string separated into two parts by @ symbol, a “personal_info” and a domain, that is personal_info@domain."
			return render_template('message.html', msg=msg)

		elif(password!=repassword):
			msg='Both passwords are not matching!'
			return render_template('message.html', msg=msg)

		else:
			cursor.execute('INSERT INTO userdata VALUES (NULL, % s, % s, % s, %s, %s)', (username, password, email, location, age))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM userdata WHERE email = % s AND password = % s', (email, password, ))
			account = cursor.fetchone()
			session['loggedin'] = True
			session['id'] = account['id']
			session['email'] = account['email']
			flash('Thank you for registering')
			msg = 'Logged in successfully !'
			flash('Logged in successfully !')
			if 'loggedin' in session:
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('SELECT * FROM userdata WHERE id = % s', (session['id'], ))
				account = cursor.fetchone() 
				return render_template('userprofile.html', account = account)  
	data = RatingBasedRecommendation()
	nameB, urlB, ratingB = topingenre('Business')
	nameF, urlF, ratingF = topingenre('Non-Fiction')
	nameT, urlT, ratingT = topratedcontent()
	nameA1, urlA1, ratingA1 = randombooks()
	nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
	return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)

@app.route('/userprofile.html')
def userprofile():
	#data = RatingBasedRecommendation()
	#print(data)
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM userdata WHERE id = % s', (session['id'], ))
		account = cursor.fetchone() 
		return render_template('userprofile.html', account = account)   
	data = RatingBasedRecommendation()
	nameB, urlB, ratingB = topingenre('Business')
	nameF, urlF, ratingF = topingenre('Non-Fiction')
	nameT, urlT, ratingT = topratedcontent()
	nameA1, urlA1, ratingA1 = randombooks()
	nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
	return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)

@app.route('/login.html', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		email = request.form['email']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM userdata WHERE email = % s AND password = % s', (email, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['email'] = account['email']
			flash('Thank you for registering')
			msg = 'Logged in successfully !'
			flash('Logged in successfully !')
			if 'loggedin' in session:
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('SELECT * FROM userdata WHERE id = % s', (session['id'], ))
				account = cursor.fetchone() 
				return render_template('userprofile.html', account = account)   
		else:
			msg = 'Incorrect username / password !'
			flash('Incorrect username / password !')
			return render_template('message.html', msg=msg)

	data = RatingBasedRecommendation()
	nameB, urlB, ratingB = topingenre('Business')
	nameF, urlF, ratingF = topingenre('Non-Fiction')
	nameT, urlT, ratingT = topratedcontent()
	nameA1, urlA1, ratingA1 = randombooks()
	nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
	return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)
@app.route("/update.html", methods =['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'location' in request.form and 'age' in request.form:
			username = request.form['username']
			#password = request.form['password']
			email = request.form['email']
			location = request.form['location']  
			age = request.form['age'] 
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM userdata WHERE email = % s', (email, ))
			account = cursor.fetchone()      
			cursor.execute('UPDATE userdata SET  username =% s, email =% s, location =% s, age =% s WHERE id =% s', (username, email, location, age, (session['id'], ), ))
			mysql.connection.commit()
			msg = 'You have successfully updated !'
			msg = 'Please fill out the form !'
			if 'loggedin' in session:
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('SELECT * FROM userdata WHERE id = % s', (session['id'], ))
				account = cursor.fetchone() 
	return render_template('userprofile.html', account = account)   

@app.route("/updatepassword.html", methods =['GET', 'POST'])
def updatepassword():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'password' in request.form and 'confirmpassword' in request.form:
			password = request.form['password']
			#password = request.form['password']
			confirmpassword = request.form['confirmpassword']
			if 'loggedin' in session:
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('SELECT * FROM userdata WHERE id = % s', (session['id'], ))
				account = cursor.fetchone()
			if(account['password']==password):
				msg = 'New Password cannot Be the Old One!'
				return render_template('message.html', msg=msg)
			if(password!=confirmpassword):
				msg = 'Both Passwords Must be Same!'
				return render_template('message.html', msg=msg)
			if(password==confirmpassword):     
				cursor.execute('UPDATE userdata SET  password =% s WHERE id =% s', (password, (session['id'], ), ))
				mysql.connection.commit()
				session.pop('loggedin', None)
				session.pop('id', None)
				session.pop('username', None)
				data = RatingBasedRecommendation()
				nameB, urlB, ratingB = topingenre('Business')
				nameF, urlF, ratingF = topingenre('Non-Fiction')
				nameT, urlT, ratingT = topratedcontent()
				nameA1, urlA1, ratingA1 = randombooks()
				nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
				return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)
			else:
				msg = 'You have successfully updated !'
				msg = 'Please fill out the form !'
				if 'loggedin' in session:
					cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
					cursor.execute('SELECT * FROM userdata WHERE id = % s', (session['id'], ))
					account = cursor.fetchone() 
	return render_template('userprofile.html', account = account)   

@app.route('/contactus.html')
def contactus():
	#data = RatingBasedRecommendation()
	#print(data)
	return render_template('celebritylist.html')
@app.route('/aboutus.html')
def aboutus():
	#data = RatingBasedRecommendation()
	#print(data)
	return render_template('landing.html')


@app.route('/logout.html')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	data = RatingBasedRecommendation()
	nameB, urlB, ratingB = topingenre('Business')
	nameF, urlF, ratingF = topingenre('Non-Fiction')
	nameT, urlT, ratingT = topratedcontent()
	nameA1, urlA1, ratingA1 = randombooks()
	nameA2, urlA2, ratingA2 = randombooks()
	#print(data)
	return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)
	#return render_template('index.html')
'''
@app.route('/home.html')
def home():
	return render_template('home.html')

@app.route('/login.html')
def login():
	return render_template('login.html')

@app.route('/RatingBased.html')
def rating():
	data = RatingBasedRecommendation()
	#print(data)
	return render_template('RatingBased.html', result = data)

'''
@app.route('/forgotpassword.html')
def forgotpassword():
	return render_template('forgotpassword.html')

@app.route("/emailpassword.html", methods=['GET', 'POST'])
def emailpassword():
	msg = ''
	if request.method == 'POST' and 'email' in request.form:
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM userdata WHERE email = % s', (email, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists!'
			msg = Message(
							'Login Password for {}'.format(account['email']),
							sender ='saurabhmishra.mylibrary@gmail.com',
							recipients = [account['email']]
						)
			msg.body = "Hello {0},\nHere is the Login Password for your Acoount with email address as {1}.\nKindly login using the same password.\nPassword: {2}\nThanking You,\nSaurabh Mishra".format(account['username'], account['email'], account['password'])
			mail.send(msg)
			data = RatingBasedRecommendation()
			nameB, urlB, ratingB = topingenre('Business')
			nameF, urlF, ratingF = topingenre('Non-Fiction')
			nameT, urlT, ratingT = topratedcontent()
			nameA1, urlA1, ratingA1 = randombooks()
			nameA2, urlA2, ratingA2 = randombooks()
			#print(data)
			return render_template('index.html', result = data, nameB=nameB, urlB=urlB, ratingB=ratingB, nameF=nameF, urlF=urlF, ratingF=ratingF, nameT=nameT, urlT=urlT, ratingT=ratingT, nameA1=nameA1, urlA1=urlA1, ratingA1=ratingA1, nameA2=nameA2, urlA2=urlA2, ratingA2=ratingA2)
		else:
			msg='Account Does Not Exists!'
			return render_template('message.html', msg=msg)

if (__name__ == "__main__"):
	app.run(debug = True)
