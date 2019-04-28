import datetime

# Class to hold database data for a single encounter at the HIV Alliance
class Encounter(object):
	def Populate(self, databaseJson):
		if databaseJson:
			if ('today' in databaseJson):
				self.today = databaseJson['today']

			if ('staff_role' in databaseJson):
				self.staff_role = databaseJson['staff_role']

			if ('staff_initials' in databaseJson):
				self.staff_initials = databaseJson['staff_initials']

			if ('location' in databaseJson):
				self.location = databaseJson['location']

			if ('has_used_shared_needles' in databaseJson):
				self.has_used_shared_needles = databaseJson['has_used_shared_needles']

			if ('months_since_hiv_test' in databaseJson):
				self.months_since_hiv_test = databaseJson['months_since_hiv_test']

			if ('months_since_hepc_test' in databaseJson):
				self.months_since_hepc_test = databaseJson['months_since_hepc_test']

			if ('has_any_medical_condition' in databaseJson):
				self.has_any_medical_condition = databaseJson['has_any_medical_condition']

			if ('wants_injection_info' in databaseJson):
				self.wants_injection_info = databaseJson['wants_injection_info']

			if ('wants_treatment_info' in databaseJson):
				self.wants_treatment_info = databaseJson['wants_treatment_info']

			if ('syringes_brought_in' in databaseJson):
				self.syringes_brought_in = databaseJson['syringes_brought_in']

			if ('syringes_taken' in databaseJson):
				self.syringes_taken = databaseJson['syringes_taken']

			if ('alcohol_swabs_taken' in databaseJson):
				self.alcohol_swabs_taken = databaseJson['alcohol_swabs_taken']

			if ('condoms_taken' in databaseJson):
				self.condoms_taken = databaseJson['condoms_taken']

			if ('sharps_taken' in databaseJson):
				self.sharps_taken = databaseJson['sharps_taken']

			if ('cottons_taken' in databaseJson):
				self.cottons_taken = databaseJson['cottons_taken']

			if ('is_homeless' in databaseJson):
				self.is_homeless = databaseJson['is_homeless']

			if ('health_insurance_provider' in databaseJson):
				self.health_insurance_provider = databaseJson['health_insurance_provider']

			if ('has_exchanged_previously' in databaseJson):
				self.has_exchanged_previously = databaseJson['has_exchanged_previously']

			if ('witnessed_od_last_year' in databaseJson):
				self.witnessed_od_last_year = databaseJson['witnessed_od_last_year']

			if ('people_exchanging_needles_for' in databaseJson):
				self.people_exchanging_needles_for = databaseJson['people_exchanging_needles_for']

			if ('has_recieved_food' in databaseJson):
				self.has_recieved_food = databaseJson['has_recieved_food']

			if ('client_id' in databaseJson):
				self.client_id = str(databaseJson['client_id'])

			if ('_id' in databaseJson):
				self._id = str(databaseJson['_id'])


	def Randomize(self):
		import random
		import string
		from datetime import datetime, timedelta, timezone

		step = timedelta(days=1)
		start = datetime(2013, 1, 1, tzinfo=timezone.utc)
		end = datetime.now(timezone.utc)
		random_date = start + random.randrange((end - start) // step + 1) * step

		year = random.randint(1990, 2019)
		month = random.randint(1, 12)
		day = random.randint(1, 31)
		self.today = "%s-%s%s-%s%s" % (year, "0" if month < 10 else "", month, "0" if day < 10 else "", day)
		self.staff_role = "Staff" if bool(random.getrandbits(1)) else "Volunteer/Intern"

		self.staff_initials = ''.join(random.choice(string.ascii_uppercase) for x in range(3))

		locations = ['Blair', 'HIV A', 'Glenwood', 'Cottage Grove', 'Outreach']
		self.location = random.choice(locations)

		healthInsuranceProviders = ['Veterans Benefits', 'Medicare', 'OHP', 'Private Insurance', 'Other', 'None']
		self.health_insurance_provider = random.choice(locations)

		self.has_used_shared_needles = bool(random.getrandbits(1))
		self.has_any_medical_condition = bool(random.getrandbits(1))
		self.wants_injection_info = bool(random.getrandbits(1))
		self.wants_treatment_info = bool(random.getrandbits(1))
		self.is_homeless = bool(random.getrandbits(1))
		self.has_exchanged_previously = bool(random.getrandbits(1))
		self.witnessed_od_last_year = bool(random.getrandbits(1))
		self.has_recieved_food = bool(random.getrandbits(1))

		maxRandomNumber = 100
		self.months_since_hiv_test = random.randint(0, maxRandomNumber)
		self.months_since_hepc_test = random.randint(0, maxRandomNumber)
		self.syringes_brought_in = random.randint(0, maxRandomNumber)
		self.syringes_taken = random.randint(0, maxRandomNumber)
		self.alcohol_swabs_taken = random.randint(0, maxRandomNumber)
		self.condoms_taken = random.randint(0, maxRandomNumber)
		self.sharps_taken = random.randint(0, maxRandomNumber)
		self.cottons_taken = random.randint(0, maxRandomNumber)
		self.people_exchanging_needles_for = random.randint(0, maxRandomNumber)

	def __repr__(self):
		str_repr = "## Encounter Object ##\n"
		for key in self.__dict__.keys():
			str_repr += "{}: {}\n".format(key, self.__dict__[key])
		return str_repr
