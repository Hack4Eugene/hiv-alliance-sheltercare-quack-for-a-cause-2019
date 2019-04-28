#####################
### Dependencies  ###
#####################
from flask import Flask, request, render_template, redirect, url_for
from DatabaseClasses.Encounter import Encounter
from DatabaseClasses.Client import Client
import sweat_db
import os
import re
import json
import time

################
### Globals  ###
################
app = Flask(__name__)
db = sweat_db.HivAllianceDb()

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

#########################
### Helper Functions  ###
#########################
def GetMetricsAboutQuery(clientList):
	start_time = time.time()
	total_syringes_returned = 0
	total_syringes_taken = 0
	unique_visits = 0
	total_encounters = 0

	average_encounters_per_client = 0
	average_syringes_returned_per_client = 0
	average_syringes_taken_per_client = 0

	for client in clientList:
		if ('encounter_ids' in client):
			for encounter_id in client['encounter_ids']:
				encounter = db.get_encounter_by_id(encounter_id)
				total_encounters += 1
				total_syringes_taken += encounter.syringes_taken
				total_syringes_returned += encounter.syringes_brought_in

		unique_visits += 1

	if (unique_visits > 0):
		average_encounters_per_client = total_encounters / unique_visits
		average_syringes_taken_per_client = total_syringes_taken / unique_visits
		average_syringes_returned_per_client = total_syringes_returned / unique_visits

	returnJson = {
		'total_syringes_returned' : total_syringes_returned, 
		'total_syringes_taken' : total_syringes_taken,
		'unique_visits' : unique_visits,
		'total_encounters' : total_encounters,
		'average_encounters_per_client' : average_encounters_per_client,
		'average_syringes_returned_per_client' : average_syringes_returned_per_client,
		'average_syringes_taken_per_client' : average_syringes_returned_per_client
	}

	elapsed_time = time.time() - start_time
	print("Time to generate data metrics: " + str(elapsed_time))
	return returnJson


###############
### Routes  ###
###############
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def loginPage():
	global logged_in_user
	if (logged_in_user):
		return redirect('/clientSearch')
	if ('username' in request.form and 'password' in request.form):
		if (request.form['username'] == admin_username and request.form['password'] == admin_password):
			logged_in_user = admin_username
			return redirect('/clientSearch')
		elif (request.form['username'] == staff_username and request.form['password'] == staff_password):
			logged_in_user = staff_username
			return redirect('/clientSearch')
		else:
			return render_template('login.html', error='Invalid login credentials')
	else:
		return render_template('login.html', error='Please enter both a username and a password')


@app.route('/logout')
def logout():
	global logged_in_user
	logged_in_user = ""
	return redirect('/login')


@app.route('/clientCreate', methods=['GET'])
def client_create():
	global logged_in_user
	if (not logged_in_user):
		return render_template('login.html')
	client = Client()
	client.Populate(request.args)
	return render_template('clientForm.html', new_client_string=json.dumps(client.__dict__, default=str))


@app.route('/encounterCreate', methods=['GET'])
def encounter_create():
	global logged_in_user
	if (not logged_in_user):
		return render_template('login.html')
	client_id = request.args.get('client_id')
	if not client_id:
		print("ERROR: client_id cannot be none when visiting encounterCreate page")
		return redirect('/clientSearch')
	return render_template('encounterForm.html', client_id=client_id)


@app.route('/clientEdit', methods=['GET'])
def client_edit():
	global logged_in_user
	if (not logged_in_user):
		return render_template('login.html')

	client_id = request.args.get('client_id')
	client = db.get_client_by_id(client_id)
	return render_template('clientForm.html', client_string=json.dumps(client.__dict__, default=str))


@app.route('/encounterEdit', methods=['GET'])
def encounter_edit():
	global logged_in_user
	if (not logged_in_user):
		return render_template('login.html')

	encounter_id = request.args.get('encounter_id')
	if (logged_in_user == staff_username):
		return redirect('/')

	encounter = db.get_encounter_by_id(encounter_id)
	return render_template('encounterForm.html', encounter_string=json.dumps(encounter.__dict__, default=str))

@app.route('/encounter', methods=['POST'])
def encounter_post():
	global logged_in_user
	if (not logged_in_user):
		return render_template('login.html')

	encounter = Encounter()
	encounter.Populate(request.form)
	db.insert_encounter(encounter)
	client_id = encounter.client_id
	return redirect('/client?client_id=' + str(client_id))


@app.route('/encounter', methods=['PUT'])
def encounter_put():
	global logged_in_user
	if (not logged_in_user):
		return render_template('login.html')

	encounter = Encounter()
	encounter.Populate(request.form)
	encounter_id = encounter._id
	db.update_encounter(encounter)
	encounter = db.get_encounter_by_id(encounter_id)
	client_id = encounter.client_id
	return url_for('client_get', client_id=client_id)


@app.route('/client', methods=['GET'])
def client_get():
	global logged_in_user
	if (not logged_in_user):
		return render_template('login.html')

	client_id = request.args.get('client_id')
	client = db.get_client_by_id(client_id)
	encounters = db.get_encounters_by_client_id(client_id)
	return render_template('detailClientPage.html', client_info=client, encounters=encounters, is_admin=logged_in_user == admin_username)


@app.route('/client', methods=['POST'])
def client_post():
	global logged_in_user
	if (not logged_in_user):
		return render_template('login.html')

	client = Client()
	client.Populate(request.form)
	client_id = db.insert_client(client)
	return redirect('/client?client_id=' + str(client_id))


@app.route('/client', methods=['PUT'])
def client_put():
	global logged_in_user
	if (not logged_in_user):
		return render_template('login.html')

	client = Client()
	client.Populate(request.form)
	client_id = db.update_client(client)
	return url_for('client_get', client_id=client_id)


@app.route('/clientSearchQuery', methods=['GET'])
def client_search_query():
	query = {}

	if ('_id' in request.args and request.args['_id']):
		query['_id'] = request.args['_id']

	if ('last_name' in request.args and request.args['last_name']):
		query['last_name'] = request.args['last_name']

	if ('city' in request.args and request.args['city']):
		query['city'] = request.args['city']

	if ('birthdate' in request.args and request.args['birthdate']):
		query['birthdate'] = request.args['birthdate']

	if ('sex' in request.args and request.args['sex']):
		query['sex'] = request.args['sex']

	if ('gender' in request.args and request.args['gender']):
		query['gender'] = request.args['gender']

	if ('ethnicity' in request.args and request.args['ethnicity']):
		query['ethnicity'] = request.args['ethnicity']

	if ('race' in request.args and request.args['race']):
		query['race'] = request.args['race']

	if ('zipcode' in request.args and request.args['zipcode']):
		query['zipcode'] = request.args['zipcode']

	keys = query.keys()
	for key in keys:
		query[key] = re.compile(query[key], re.IGNORECASE)

	clients = []
	clientEntries = db.db.clients.find(query)
	for clientEntry in clientEntries:
		client = Client()
		client.Populate(clientEntry)
		clients.append(client.__dict__)

	# This takes a lot of time
	#listMetrics = GetMetricsAboutQuery(clients)
	return json.dumps(clients, default=str)

@app.route('/clientSearch', methods=['GET'])
def client_search():
	global logged_in_user
	if (not logged_in_user):
		return render_template('login.html')

	return render_template('clientSearch.html')

@app.route('/encounterSearchQuery', methods=['GET'])
def encounter_search_query():
	query = {}

	for arg in request.args:
                val = request.args.get(arg)
                if val:
                    query[arg] = val
       
	keys = query.keys()
	for key in keys:
		query[key] = re.compile(query[key], re.IGNORECASE)

	encounters = []
	encounterEntries = db.db.encounters.find(query)
	for encounterEntry in encounterEntries:
		encounter = Encounter()
		encounter.Populate(encounterEntry)
		encounters.append(encounter.__dict__)

	return json.dumps(encounters, default=str)

@app.route('/report')
def reportPage():
	global logged_in_user
	if (not logged_in_user):
		return render_template('login.html')
	return render_template('report.html')
