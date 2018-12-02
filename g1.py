import os, httplib2, json, argparse
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
from googleapiclient.discovery import build
from apiclient import errors
import requests
import json

# Make authorized API calls by using OAuth 2.0 client ID credentials for authentication & authorization
parser = argparse.ArgumentParser(parents=[tools.argparser])
flags = parser.parse_args()
flow = flow_from_clientsecrets('client_secrets.json',
    scope='https://www.googleapis.com/auth/plus.business.manage',
    redirect_uri='https://myopip.com')

# For retrieving the refresh token
flow.params['access_type'] = 'offline'
flow.params['approval_prompt'] = 'force' 

# Use a Storage in current directory to store the credentials in
storage = Storage('.' + os.path.basename(__file__))
credentials = storage.get()

# credentials = tools.run_flow(flow, storage, flags) 
# storage.put(credentials)
# Acquire credentials in a command-line application
if credentials is None or credentials.invalid:
 credentials = tools.run_flow(flow, storage, flags) 
 storage.put(credentials)

# Apply necessary credential headers to all requests made by an httplib2.Http instance
http = credentials.authorize(httplib2.Http())

# Refresh the access token if it expired
if credentials is not None and credentials.access_token_expired:
 try:
   credentials.refresh(http)
   storage.put(credentials)
 except:
   pass

access_token = credentials.token_response["access_token"]

print(f"Access token:{access_token}")
headers = {
    'authorization': "Bearer " + access_token,
    'content-type': "application/json",
}

print("Listing accounts..")
url = 'https://mybusiness.googleapis.com/v4/accounts'
response = requests.get(url, headers=headers)
print(f"Status code: {response.status_code}")
print(f"Status text: {response.text}")



