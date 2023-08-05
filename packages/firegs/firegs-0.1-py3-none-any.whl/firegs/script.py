import os
import requests
import json
import configparser
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import argparse
import webbrowser

# Firebase project ID
PROJECT_ID = 'ar-common'

# Path to the service account key file
SERVICE_ACCOUNT_FILE = None

# Determine the location of the configuration file
config_file = os.path.expanduser('~/.firegs_config')

# Create a ConfigParser object
config = configparser.ConfigParser()

# Check if the configuration file exists
if os.path.exists(config_file):
    # If it exists, read it
    config.read(config_file)

    # Get the service account file path
    SERVICE_ACCOUNT_FILE = config.get('DEFAULT', 'service_account_file')
else:
    # If it does not exist, prompt the user to enter the path
    SERVICE_ACCOUNT_FILE = input('Please enter the path to your service account file: ')

    # Save the path to the configuration file for future use
    config['DEFAULT'] = {'service_account_file': SERVICE_ACCOUNT_FILE}
    with open(config_file, 'w') as f:
        config.write(f)

# API endpoint for creating apps
CREATE_APP_URL = f"https://firebase.googleapis.com/v1beta1/projects/{PROJECT_ID}/androidApps"

# API endpoint for listing apps
LIST_APPS_URL = f"https://firebase.googleapis.com/v1beta1/projects/{PROJECT_ID}/androidApps"

# Firebase project URL
FIREBASE_PROJECT_URL = f"https://console.firebase.google.com/project/{PROJECT_ID}/settings/general"

# Parse command line arguments
parser = argparse.ArgumentParser(description='Manage Firebase Android Apps')
parser.add_argument('-c', '--create', help='Create an app with the provided Application ID or package name')
parser.add_argument('-d', '--display', help='Display name for the app')
parser.add_argument('-l', '--list', help='List all apps in the project', action='store_true')
args = parser.parse_args()

# Load credentials from the service account file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=['https://www.googleapis.com/auth/cloud-platform'],
)

# Create an authorized session
authed_session = AuthorizedSession(credentials)

# Create a new Android app
if args.create:
    app_id = args.create
    display_name = args.display if args.display else app_id  # Use the app ID as the display name if no display name is provided
    payload = {
        'packageName': app_id,
        'displayName': display_name,
    }

    try:
        response = authed_session.post(CREATE_APP_URL, json=payload)
        response.raise_for_status()
        print(f'Successfully created the Android app with ID/package name: {app_id} and Display name: {display_name}')

        # Open Firebase project page in browser
        webbrowser.open(FIREBASE_PROJECT_URL)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 409:
            print(f'The Android app with ID/package name: {app_id} already exists in the Firebase project.')
        else:
            print(f'Error creating the Android app: {e}')

elif args.list:
    # Initialize an empty list to store all apps
    all_apps = []

    # Initialize nextPageToken to None for the first API call
    next_page_token = None

    while True:
        # Create the API URL with the nextPageToken parameter if it is not None
        list_apps_url = LIST_APPS_URL
        if next_page_token is not None:
            list_apps_url += f'?pageToken={next_page_token}'

        # Call the API
        response = authed_session.get(list_apps_url)
        response.raise_for_status()
        apps = response.json()

        # Add the apps from the current page to the all_apps list
        all_apps.extend(apps['apps'])

        # If a nextPageToken is present in the response, set it for the next API call
        if 'nextPageToken' in apps:
            next_page_token = apps['nextPageToken']
        else:
            # If no nextPageToken is present, we have fetched all apps, so we break the loop
            break

    # Now all_apps contains all Android apps in the project
    for app in all_apps:
        display_name = app.get('displayName', 'No display name')
        print(f'  - {display_name} ({app["packageName"]})')
