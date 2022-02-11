'''
> pip3 install requests
> python3 domain_availability_checker.py --help
> python3 domain_availability_checker.py google.com
> python3 domain_availability_checker.py test.com
> python3 domain_availability_checker.py bkash.com
'''

import time
import requests
import argparse
import pprint

# pprint setup
pp = pprint.PrettyPrinter(indent=4)

# setup cli domain argument
parser = argparse.ArgumentParser(description="Check domain for availability")
parser.add_argument("domain", type=str, help="Domain name to be checked")
args = parser.parse_args()

# print(args)

# godaddy API credentials for authorization
api_key = "putyourownapikey"
api_secret = "putyourownapisecret"
req_headers = {
    "Authorization": f"sso-key {api_key}:{api_secret}",
    "accept": "application/json"
}

# assemble the request url with the given domain
def get_req_url(check_domain):
    return f"https://api.ote-godaddy.com/v1/domains/available?domain={check_domain}"

def check_domain_availability(check_domain):
    print(f"Checking the availability of domain {check_domain}")
    req_url = get_req_url(check_domain)

    # without headers, it will return status code 401. So try to add headers, even if it optional.
    req = requests.get(req_url, headers=req_headers)

    # if the request was unsuccessful, notify the user and stop
    if req.status_code != 200:
        print(f"Domain URL error/Not Available: {check_domain} - Status Code {req.status_code}")
        return

    # check if the domain is available
    #print(f"Checking ... {check_domain}")
    response = req.json()
    if response["available"] == True:
        print(f"Domain {check_domain} is available for purchase")
    else:
        print(f"{time.strftime('%Y-%m-%d %H:%M')} - Domain {check_domain} is not available for purchase")

    # Let user see the the details of response
    user_response = input("Do you want to see details: [Y/N]").lower()
    if user_response == "y":
        pp.pprint(response)



check_domain_availability(args.domain)

