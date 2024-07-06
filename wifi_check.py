import requests # used to make HTTP requests in Python
import schedule # allows scheduling tasks to run at specific intervals
import time # used to handle time-related tasks like sleeping the script for a specific duration

# Function to check Wi-Fi connection
def check_wifi_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return response.status_code == 200 # If the request is successful and returns a status code of 200, it returns True
    except requests.ConnectionError:
        return False # If a requests.ConnectionError is encountered (indicating no internet connection), it returns False

# Function to make a call using Sinch
def make_call():
    key = "abcd1234efgh5678ijkl9012mnop3456" # Sinch API credentials
    secret = "1234abcd5678efgh9012ijkl3456mnop" # Sinch API credentials
    from_number = "+12345678901" # phone numbers
    to = "+19876543210" # phone numbers
    locale = "en-US" # language for the text-to-speech message
    url = "https://calling.api.sinch.com/calling/v1/callouts" # endpoint for making callouts with Sinch

    # Dictionary contains the call details including the caller ID (cli), the destination number, the locale, and the text message to be spoken
    payload = { 
      "method": "ttsCallout",
      "ttsCallout": {
        "cli": from_number,
        "destination": {
          "type": "number",
          "endpoint": to
        },
        "locale": locale,
        "text": "Your Wi-Fi connection is down. Please check it."
      }
    }

    headers = {"Content-Type": "application/json"} # specifies that the request content type is JSON

    response = requests.post(url, json=payload, headers=headers, auth=(key, secret)) # sends the POST request with the payload and headers, authenticated with the Sinch credentials

    data = response.json()
    print(data)

# Function to be scheduled
def job():
    if not check_wifi_connection():
        make_call()

# Schedule the job to run every 2 minutes
schedule.every(2).minutes.do(job)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
