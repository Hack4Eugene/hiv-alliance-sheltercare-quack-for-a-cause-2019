# Class to hold database data for a single encounter at the HIV Alliance
class Client(object):
	def Populate(self, clientForm):
		if clientForm:
			if ('last_name' in clientForm):
				self.last_name = clientForm['last_name']

			if ('city' in clientForm):
				self.city = clientForm['city']

			if ('birthdate' in clientForm):
				self.birthdate = clientForm['birthdate']

			if ('sex' in clientForm):
				self.sex = clientForm['sex']

			if ('gender' in clientForm):
				self.gender = clientForm['gender']

			if ('ethnicity' in clientForm):
				self.ethnicity = clientForm['ethnicity']

			if ('race' in clientForm):
				self.race = clientForm['race']

			if ('zipcode' in clientForm):
				self.zipcode = clientForm['zipcode']

			if ('_id' in clientForm):
				self._id = clientForm['_id']

			if ('encounter_ids' in clientForm):
				self.encounter_ids = clientForm['encounter_ids']
			else:
				self.encounter_ids = []


	def Randomize(self):
		import random
		import string
		from datetime import datetime, timedelta, timezone

		self.last_name = ''.join(random.choice(string.ascii_uppercase) for x in range(2))

		locations = ['Seattle', 'Eugene', 'Springfield', 'Portland', 'San Francisco', 'New York', 'Miami', 'Paris', 'London']
		self.city = random.choice(locations)[0:2].upper()

		birth_year = random.randint(1930, 2012)
		birth_month = random.randint(1, 12)
		birth_jeff_is_the_worst = random.randint(1, 31)
		self.birthdate = "%s-%s%s-%s%s" % (birth_year, "0" if birth_month < 10 else "", birth_month, "0" if birth_jeff_is_the_worst < 10 else "", birth_jeff_is_the_worst)

		sex_at_birth_options = ['Male', 'Female', 'Intersex', 'Other']
		self.sex = random.choice(sex_at_birth_options)

		gender_options = ['Male', 'Female', 'Non-binary', 'Other']
		self.gender = random.choice(gender_options)

		enthnicity_options = ['Hispanic/Latino', 'Non-Hispanic/Latino', 'Other']
		self.ethnicity = random.choice(enthnicity_options)

		race_options = ['Black/African American', 'Asian', 'Native Hawaiian/Pacific Islander', 'American Indian/Alaskan Native', 'White', 'Multiracial']
		self.race = random.choice(race_options)

		self.zipcode = ''.join(random.choice(string.digits) for x in range(5))

	def __repr__(self):
		str_repr = "## Client Object ##\n"
		for key in self.__dict__.keys():
			str_repr += "{}: {}\n".format(key, self.__dict__[key])
		return str_repr
