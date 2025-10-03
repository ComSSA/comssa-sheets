import os

import requests
from dotenv import load_dotenv

from google.oauth2 import service_account 
from googleapiclient.discovery import build

def main():
    # loading environmental variables
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] 


    load_dotenv()
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    CTFD_TOKEN = os.getenv("CTFD_TOKEN")
    CTFD_URL = os.getenv("CTFD_URL")
    
    #connecting to google sheets with service-account.json
    credentials = service_account.Credentials.from_service_account_file(
        'service-account.json', scopes=SCOPES)
    sheets_client = build('sheets', 'v4', credentials=credentials)

    #Need to get all users


    #Get further user info


    #Write to range


def send_alert(message: str):
    DISCORD_WEBHOOK := os.Getenv("DISCORD_WEBHOOK")
    DISCORD_ID_TO_PING := os.Getenv("DISCORD_ID_TO_PING")
    pass

def get_users(url: str, token: str):
    """
    Remember to paginate this
    """
    pass


def get_user_data(url: str, token: str, userID: int):
    """
    Gets user data based on list of user ids from get_users
    """
    pass

def update_sheet(service, spreadsheet_id: str, write_range: str, values: list):
    """
    Updates google sheets with user data
    """
    pass


if __name__ == "__main__":
    main()
