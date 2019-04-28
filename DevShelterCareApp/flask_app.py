#####################
### Dependencies  ###
#####################
from flask import Flask, request, render_template, redirect

################
### Globals  ###
################
app = Flask(__name__)

# Constants
DebugMode = "DEBUG"
ReleaseMode = "RELEASE"
admin_username = "admin"
admin_password = "admin"
staff_username = "staff"
staff_password = "staff"

DeployMode = DebugMode # Either DebugMode or ReleaseMode
logged_in_user = admin_username if DeployMode == DebugMode else ""
print("Starting flask app in " + DeployMode + " mode")

###############
### Routes  ###
###############
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def loginPage():
	global logged_in_user
	if (logged_in_user):
		return redirect('/report')
	elif (request.method == 'GET'):
		return render_template('login.html')

	if ('username' in request.form and 'password' in request.form):
		if (request.form['username'] == admin_username and request.form['password'] == admin_password):
			logged_in_user = admin_username
			return redirect('/report')
		elif (request.form['username'] == staff_username and request.form['password'] == staff_password):
			logged_in_user = staff_username
			return redirect('/report')
		else:
			return render_template('login.html', error='Invalid login credentials')
	else:
		return render_template('login.html', error='Please enter both a username and a password')

@app.route('/logout')
def logout():
	global logged_in_user
	logged_in_user = ""
	return redirect('/login')

@app.route('/report')
def report():
	global logged_in_user
	if (not logged_in_user):
		return redirect('/login')

	return render_template('issueForm.html')

@app.route('/submitReport')
def submit_report():
	global logged_in_user
	if (not logged_in_user):
		return redirect('/login')

	pass

