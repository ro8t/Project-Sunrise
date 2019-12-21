# Dependencies
import requests
import json
from pprint import pprint
import os
import urllib.request as request
# from linkedin import linkedin
# from oauthlib import *

# API Keys
from config import authentic, linkedin_cid, linkedin_cs, linkedin_state_key, crunchbase

# Establishing API connection
base_url = f"https://authenticjobs.com/api/?api_key={authentic}"
form = "&format=json"

# Multi-option parameters
categories_call = requests.get(f"{base_url}&method=aj.categories.getList{form}").json()
categories = categories_call["categories"]["category"]
# pprint(categories)
# print()

type_call = requests.get(f"{base_url}&method=aj.types.getList{form}").json()
job_types = type_call["types"]["type"]
# pprint(job_types)

# Method: just job id
def job_id(jid):
    get_job = requests.get(f"{base_url}&method=aj.jobs.get&id={jid}{form}").json()
    company = {
        "Name": get_job["listing"]["company"]["name"],
        "Title": get_job["listing"]["title"],
        "Term": get_job["listing"]["type"]["name"]
    }
    return company

# Method: Job search
''' Parameters to use:
category: The id of a job category to limit to. See aj.categories.getList
type: The id of a job type to limit to. See aj.types.getList
sort: Accepted values are: date-posted-desc (the default) and date-posted-asc
company: Free-text matching against company names
         >> (Suggested values are the ids from aj.jobs.getCompanies)
location: Free-text matching against company location names
         >> (Suggested values are the ids from aj.jobs.getLocation)
telecommuting: Set to 1 if you only want telecommuting jobs
keywords: Keywords to look for in the title or description of the job posting
         >> (Separate multiple keywords with commas)
         >> (Multiple keywords will be treated as an OR)
begin_date: Unix timestamp. Listings posted before this time will not be returned
end_date: Unix timestamp. Listings posted after this time will not be returned
page: The page of listings to return. Defaults to 1.
perpage: The number of listings per page. The default value is 10. The maximum value is 100.
'''
def job_search(category=None, tiep=None, sort=None, company=None, location=None, 
               telecommuting=None, keywords=None, begin_date=None, end_date=None, 
               company_type=None, page=None, perpage=None):
    # New base
    call = base_url + "&method=aj.jobs.search" + form
    
    # Adding chosing attributes
    if category != None:
        call += f"&category={category}"
    if tiep != None:
        call += f"&type={tiep}"
    if sort != None:
        call += f"&sort={sort}"
    if company != None:
        call += f"&company={company}"
    if location != None:
        call += f"&location={location}"
    if telecommuting != None:
        call += f"&telecommuting={telecommuting}"
    if keywords != None:
        call += f"&keywords={keywords}"
    if begin_date != None:
        call += f"&begin_date={begin_date}"
    if end_date != None:
        call += f"&end_date={end_date}"
    if company_type != None:
        call += f"&company_type{company_type}"
    if page != None:
        call += f"&page={page}"
    if perpage != None:
        call += f"&perpage={perpage}"
    
    search = requests.get(call).json()
    return search
# request = requests.get(f"https://authenticjobs.com/api/?api_key={authentic}&method=aj.jobs.search&company_type=5{form}").json()
# company_names = []
request = job_search(category="4", company_type="5", keywords="HTML,Javascript")
# for company in request["listings"]["listing"]:
#     company_names.append(company["company"]["name"])
# print(company_names)
company_locations =[]
try:
    for company in request["listings"]["listing"]:
        company_locations.append(company["company"]["location"]["name"])
except KeyError:
    company_locations.append("missing")

print(company_locations)

# pprint(job_search(category="4, 2", page="1", perpage="5"))

# Clearbit API | Logo's








# LinkedIn API Call

# linkedin_api_accessToken = "https://www.linkedin.com/oauth/v2/accessToken/"
# linkedin_api_auth = "https://www.linkedin.com/oauth/v2/authorization"
# linkedin_data_get = {
#     "response_type": "code",
#     "client_id": linkedin_cid,
#     "redirect_uri": "https://www.google.com/",
#     "state": linkedin_state_key,
#     "scope": "r_liteprofile%20r_emailaddress%20w_member_social"
#     # "client_secret": linkedin_cs
# }

# "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={linkedin_cid}&redirect_uri=https://www.google.com/&state={linkedin_state_key}&scope=r_liteprofile%20r_emailaddress%20w_member_social"

# linkedin_auth_code = requests.get(url=linkedin_api_auth, data=linkedin_data_get)
# pprint(json.dumps(linkedin_auth_code.text))

# linkedin_access_token = requests.post(url=linkedin_api_endpoint, data=linkedin_data)
# pprint(json.dumps(linkedin_access_token.text))

# linkedin_test = requests.get(f"{linkedin_base_url}/job-search?job-title=Software+Engineer")
# pprint(linkedin_test) # 401

# Crunchbase API Call

# crunchbase_burl = f"https://api.crunchbase.com/v3.1/odm-organizations?user_key={crunchbase}"

# cb_params = {
#     "name":"google",
#     }

# response = requests.get(url=crunchbase_burl, params=cb_params)

# pprint(json.dumps(response.text))






