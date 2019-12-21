# Dependencies
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, DateTime, desc, asc

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect, 
    url_for)

from flask_sqlalchemy import SQLAlchemy

# DateTime config
from datetime import datetime
timestamp = 1545730073

# Job search api function
from job import job_search

# DataFrames
# from apis/finance import cities_gdp, cpi_df
# from apis/life import yelp_df

# Creating Flask app
app = Flask(__name__)

# Attaching app to SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/db.sqlite"

db = SQLAlchemy(app)

# Creating the three databases
class userInfo(db.Model):
	__tablename__ = "Users"

	unique_id = db.Column(db.Integer, primary_key=True)
	user_moniker = db.Column(db.String(64))
	user_email = db.Column(db.String(64))
	user_password = db.Column(db.String(64))
	current_company = db.Column(db.String(64))
	time_created = db.Column(db.DateTime())

class currentState(db.Model):
	__tablename__ = "Current State"

	unique_id = db.Column(db.Integer, primary_key=True)
	user_email = db.Column(db.String(64))
	current_industry = db.Column(db.String(64))
	# current_level = db.Column(db.String(64))
	current_function = db.Column(db.String(64))
	company_type = db.Column(db.String(64))
	current_skills = db.Column(db.String(64))
	commute_start = db.Column(db.String(64))
	commute_finish = db.Column(db.String(64))
	current_company = db.Column(db.String(64))
	hobbies = db.Column(db.String(64))
	same_company = db.Column(db.String(64))

class futureState(db.Model):
	__tablename__ = "Future State"

	unique_id = db.Column(db.Integer, primary_key=True)
	user_email = db.Column(db.String(64))
	future_industries = db.Column(db.String(64))
	future_level = db.Column(db.String(64))
	future_functions = db.Column(db.String(64))
	future_titles = db.Column(db.String(64))
	future_skills = db.Column(db.String(64))
	commute_start = db.Column(db.String(64))
	commute_radius = db.Column(db.Integer)
	hobbies = db.Column(db.String(64)) # ***** might remove

## FOR DEMO ONLY
@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()

# Homepage, redirect to route-zero
@app.route("/")
def home():
    return redirect("route-zero")

# Route-zero form
@app.route("/route-zero", methods=["GET", "POST"])
def routeZero():
	if request.method == "POST":

		# Retrieving user info from html
		user_moniker = request.form["Full Name"]
		user_email = request.form["Email"]
		user_password = request.form["Password"]
		time_created = datetime.now()

		# Check to see if user exists
		email_list = []
		all_info = userInfo.query.all()
		for email in all_info:
			email_list.append(email.user_email)

		if user_email in email_list:
			return f"Account already associated with the email {user_email}"

		# Creating new row in all tables
		user = userInfo(user_moniker=user_moniker, user_email=user_email, user_password=user_password, time_created=time_created)
		current_state = currentState(user_email=user_email)
		future_state = futureState(user_email=user_email)

		db.session.add(user)
		db.session.add(current_state)
		db.session.add(future_state)

		db.session.commit()

		return redirect('route-one')

	return render_template("route-zero.html")


# Route-one form
@app.route("/route-one", methods=["GET", "POST"])
def routeOne():
	if request.method == "POST":
		
		# Retrieving user info from html
		current_industry = request.form["Industry"]
		# current_level = request.form["Level"]
		current_function = request.form["Function"]
		company_type = request.form["Title"]

		# Grabbing the users email
		email = userInfo.query.order_by(desc("time_created")).first().user_email

		# Appending user info to the table
		user = currentState.query.filter_by(user_email=email).first()
		user.current_industry = current_industry
		# user.current_level = current_level
		user.current_function = current_function
		user.company_type = company_type

		db.session.commit()

		return redirect('route-three')

	return render_template("route-one.html")

# Route-two form
#-----------------------------------------

# Route-three form
@app.route("/route-three", methods=["GET", "POST"])
def routeThree():
	if request.method == "POST":

		# Retrieving user current skills
		current_skills = request.form["Current Skills"]

		# Grabbing the users email
		email = userInfo.query.order_by(desc("time_created")).first().user_email

		# Appending user info to the table
		user = currentState.query.filter_by(user_email=email).first()
		user.current_skills = current_skills

		db.session.commit()

		return redirect('route-four')

	return render_template("route-three.html")

# Route-four form
@app.route("/route-four", methods=["GET", "POST"])
def routeFour():
	if request.method == "POST":

		# Retrieving user future skills
		future_skills = request.form["Future Skills"]

		# Grabbing the users email
		email = userInfo.query.order_by(desc("time_created")).first().user_email

		# Appending user info to the table
		user = futureState.query.filter_by(user_email=email).first()
		user.future_skills = future_skills

		db.session.commit()

		return redirect('route-six')

	return render_template("route-four.html")

# Route-five form
#-----------------------------------------

# Route-six form
@app.route("/route-six", methods=["GET", "POST"])
def routeSix():
	if request.method == "POST":

		# Retrieve user radius and retrieve max from html
		radius_choice = request.form["commute"].split(" ")
		radius_choice.remove("-") if "-" in radius_choice else radius_choice.remove("+")
		radius_choice = [int(i) for i in radius_choice]

		commute_radius = max(radius_choice)

		# Grabbing the users email
		email = userInfo.query.order_by(desc("time_created")).first().user_email

		# Appending user info to the table
		user = futureState.query.filter_by(user_email=email).first()
		user.commute_radius = commute_radius

		db.session.commit()

		return redirect('route-nine')

	return render_template("route-six.html")

# Route-seven form
#-----------------------------------------

# Route-eight form
#-----------------------------------------

# Route-nine form
@app.route("/route-nine", methods=["GET", "POST"])
def routeNine():
	if request.method == "POST":

		# Retrieving user info from html
		same_company = request.form["yes_no"]

		# Grabbing the users email
		email = userInfo.query.order_by(desc("time_created")).first().user_email

		# Appending user info to the table
		user = currentState.query.filter_by(user_email=email).first()
		user.same_company = same_company

		db.session.commit()

		return redirect('index')

	return render_template("route-nine.html")


class finalResult(db.Model):
	__tablename__ = "Final Result"

	unique_id = db.Column(db.Integer, primary_key=True)
	user_moniker = db.Column(db.String(64))
	user_email = db.Column(db.String(64))
	current_industry = db.Column(db.String(64))
	current_function = db.Column(db.String(64))
	company_type = db.Column(db.String(64))
	current_skills = db.Column(db.String(64))
	same_company = db.Column(db.String(64))
	future_skills = db.Column(db.String(64))
	commute_radius = db.Column(db.Integer)
	apply_urls = db.Column(db.String(64))
	company_names = db.Column(db.String(64))
	company_locations = db.Column(db.String(64))
	company_taglines = db.Column(db.String(64))
	company_urls = db.Column(db.String(64))
	position_titles = db.Column(db.String(64))
	position_types = db.Column(db.String(64))
	post_dates = db.Column(db.String(64))

# Final page
@app.route("/index")
def outputTable():

	# Populating Final Result table with standard info
	## Users table data
	email = userInfo.query.order_by(desc("time_created")).first().user_email
	user = userInfo.query.filter_by(user_email=email).first()

	## Current State data
	csd = currentState.query.filter_by(user_email=email).first()

	## Future State data
	fsd = futureState.query.filter_by(user_email=email).first()


	final_result = finalResult(user_email=email, user_moniker=user.user_moniker,
							   current_industry=csd.current_industry, current_function=csd.current_function, 
							   company_type=csd.company_type, current_skills=csd.current_skills, same_company=csd.same_company,
							   future_skills=fsd.future_skills, commute_radius=fsd.commute_radius)

	db.session.add(final_result)

	db.session.commit()

	# Authentic API call
	'''
	job_search(category=None, tiep=None, sort=None, company=None, location=None, 
               telecommuting=None, keywords=None, begin_date=None, end_date=None, 
               company_type=None, page=None, perpage=None)
	'''
	## Category filter
	category = []
	if finalResult.current_industry == "Design; user experience":
		category.append("3")
	elif finalResult.current_industry == "Back-end Engineering":
		category.append("2")
	elif finalResult.current_industry == "Front-end Engineering":
		category.append("4")
	elif finalResult.current_industry == "Apps":
		category.append("5")
	elif finalResult.current_industry == "Product Management":
		category.append("10")
		category.append("9")
	elif finalResult.current_industry == "Content Copywriting":
		category.append("12")
	elif finalResult.current_industry == "Marketing & Sales":
		category.append("8")
	elif finalResult.current_industry == "Customer & Community":
		category.append("11")
	elif finalResult.current_industry == "Management":
		category.append("6")
	elif finalResult.current_industry == "Miscellaneous":
		category.append("9")

	if len(category) == 1:
		category = "".join(category)
	else:
		category = ",".join(category)

	## Company type filter
	comp_type = []
	if finalResult.company_type == "Startup":
		comp_type.append("1")
	elif finalResult.company_type == "Studio":
		comp_type.append("2")
	elif finalResult.company_type == "Small business":
		comp_type.append("3")
	elif finalResult.company_type == "Mid-sized business":
		comp_type.append("4")
	elif finalResult.company_type == "Large Organization":
		comp_type.append("5")
	elif finalResult.company_type == "Educational Institution":
		comp_type.append("6")
	elif finalResult.company_type == "Non-profit":
		comp_type.append("7")

	if len(comp_type) == 1:
		comp_type = "".join(comp_type)
	else:
		comp_type = ",".join(comp_type)

	## Accessing Final Result table
	final_result_table = finalResult.query.filter_by(user_email=email).first()

	## Keywords filter
	kwargs = [final_result_table.current_skills, final_result_table.future_skills]
	kwargs = ",".join(kwargs)

	## Making the API Call
	request = job_search(category=category, company_type=comp_type, keywords=kwargs)

	## Filling Final Result table with data from API call
	### Apply urls
	apply_urls = []
	try:
		for company in request["listings"]["listing"]:
			apply_urls.append(company["apply_url"])
	except (KeyError, TypeError) as error:
		apply_urls.append("missing")
	
	apply_urls = ",".join(apply_urls)
	final_result_table.apply_urls = apply_urls

	### Company names
	company_names =[]
	try:
		for company in request["listings"]["listing"]:
			company_names.append(company["company"]["name"])
	except (KeyError, TypeError) as error:
		company_names.append("missing")
	
	company_names = ",".join(company_names)
	final_result_table.company_names = company_names

	### Company location
	company_locations =[]
	try:
		for company in request["listings"]["listing"]:
			company_locations.append(company["company"]["location"]["name"])
	except (KeyError, TypeError) as error:
		company_locations.append("missing")
	
	company_locations = ",".join(company_locations)
	final_result_table.company_locations = company_locations

	### Company tagline
	company_taglines =[]
	try:
		for company in request["listings"]["listing"]:
			company_taglines.append(company["company"]["tagline"])
	except (KeyError, TypeError) as error:
		company_taglines.append("missing")
	
	company_taglines = ",".join(company_taglines)
	final_result_table.company_taglines = company_taglines

	### Company url
	company_urls =[]
	try:
		for company in request["listings"]["listing"]:
			company_urls.append(company["company"]["url"])
	except (KeyError, TypeError) as error:
		company_urls.append("missing")
	
	company_urls = ",".join(company_urls)
	final_result_table.company_urls = company_urls

	### Position title
	position_titles =[]
	try:
		for company in request["listings"]["listing"]:
			position_titles.append(company["title"])
	except (KeyError, TypeError) as error:
		position_titles.append("missing")
	
	position_titles = ",".join(position_titles)
	final_result_table.position_titles = position_titles

	### Position type
	position_types =[]
	try:
		for company in request["listings"]["listing"]:
			position_types.append(company["type"]["name"])
	except (KeyError, TypeError) as error:
		position_types.append("missing")
	
	position_types = ",".join(position_types)
	final_result_table.position_types = position_types

	### Job post date
	post_dates =[]
	try:
		for company in request["listings"]["listing"]:
			post_dates.append(company["post_date"])
	except (KeyError, TypeError) as error:
		post_dates.append("missing")
	
	post_dates = ",".join(post_dates)
	final_result_table.post_dates = post_dates

	db.session.commit()

	return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)










