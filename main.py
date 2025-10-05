import os
import time
import json
import requests
import logging
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- Setup ---
load_dotenv(".env")
logging.basicConfig(level=logging.INFO)

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
CTFD_TOKEN = os.getenv("CTFD_TOKEN")
CTFD_URL = os.getenv("CTFD_URL")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
DISCORD_ID_TO_PING = os.getenv("DISCORD_ID_TO_PING")


# --- Send Discord alert and exit ---
def send_alert(message, err):
    if not DISCORD_WEBHOOK:
        logging.warning("DISCORD_WEBHOOK is not set")
        return

    if DISCORD_ID_TO_PING:
        message = f"<@{DISCORD_ID_TO_PING}> {message}"

    payload = {
        "content": f"{message}\n```{err}```"
    }

    try:
        resp = requests.post(DISCORD_WEBHOOK, json=payload)
        if resp.status_code not in (200, 204):
            logging.warning(f"Unexpected status code from webhook: {resp.status_code}")
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")

    os._exit(1)


# --- Get all users (non-hidden/banned) ---
def get_users(url, token):
    all_user_ids = []
    page = 1

    while True:
        headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }
        try:
            resp = requests.get(f"{url}/api/v1/users?page={page}", headers=headers)
            resp.raise_for_status()
            result = resp.json()
        except Exception as e:
            raise Exception(f"Error getting users on page {page}: {e}")
        users = result.get("data", [])
        for user in users:
            all_user_ids.append(int(user["id"]))

        pagination = result["meta"]["pagination"]
        if pagination.get("next") is None:
            break

        page += 1
        time.sleep(0.2)

    return all_user_ids


# --- Get single user data ---
def get_user_data(url, token, user_id):
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.get(f"{url}/api/v1/users/{user_id}", headers=headers)
        resp.raise_for_status()
        result = resp.json()
    except Exception as e:
        raise Exception(f"Error fetching user {user_id}: {e}")

    user = result["data"]
    username = user["name"]
    email = user["email"]
    full_name = phone = school = dietary = course = discord_user = dob = student_id = ""
    joined_discord = False

    for field in user.get("fields", []):
        field_name = field["name"]
        field_value = field["value"]

        if field_name == "Full Name":
            full_name = field_value
        elif field_name == "Phone number":
            phone = field_value
        elif field_name == "School/University":
            school = field_value
        elif field_name == "Dietary Requirements":
            dietary = field_value
        elif field_name == "Date of Birth":
            dob = field_value
        elif field_name == "Discord Username":
            discord_user = field_value
        elif field_name == "Course and Year":
            course = field_value
        elif field_name == "Student ID":
            student_id = field_value
        elif field_name == "Have you joined the Discord server?":
            joined_discord = field_value


    return [
        full_name,       
        username,      
        email,       
        phone,      
        school,     
        dietary,    
        course,         
        dob,       
        student_id,     
        discord_user,         
        joined_discord,   
    ]



# --- Update Google Sheet ---
def update_sheet(service, spreadsheet_id, write_range, values):
    body = {"values": values}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=write_range,
        valueInputOption="RAW",
        body=body
    ).execute()


# --- Main logic ---
def main():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            "service-account.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        service = build("sheets", "v4", credentials=credentials)
    except Exception as e:
        send_alert("Error creating Sheets client", e)

    try:
        user_ids = get_users(CTFD_URL, CTFD_TOKEN)
    except Exception as e:
        send_alert("Error getting users", e)

    users = []
    for user_id in user_ids:
        try:
            data = get_user_data(CTFD_URL, CTFD_TOKEN, user_id)
            users.append(data)
            time.sleep(0.2)
        except Exception as e:
            send_alert(f"Error getting user data for user {user_id}", e)

    logging.info(f"Number of users: {len(users)}")

    write_range = "TESTING!A2:K"
    try:
        update_sheet(service, SPREADSHEET_ID, write_range, users)
    except Exception as e:
        send_alert("Error updating sheet", e)


if __name__ == "__main__":
    main()
