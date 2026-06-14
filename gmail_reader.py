from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file(
        "token.json", SCOPES
    )

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )
        creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
        token.write(creds.to_json())

service = build("gmail", "v1", credentials=creds)

print("Connected to Gmail!")

results = service.users().messages().list(
    userId="me",
    q="is:unread"
).execute()

messages = results.get("messages", [])

if not messages:
    print("No emails found.")
else:
    msg_id = messages[0]["id"]

    message = service.users().messages().get(
        userId="me",
        id=msg_id
    ).execute()
    
    
    
    print(message["payload"].keys())

    headers = message["payload"]["headers"]
    

    for header in headers:
        if header["name"] == "Subject":
            print("Subject:", header["value"])
            
            import base64

parts = message["payload"]["parts"]
# for part in parts:
#     print(part["mimeType"])


for part in parts:
    if part["mimeType"] == "text/plain":

        data = part["body"]["data"]

        body = base64.urlsafe_b64decode(
            data
        ).decode("utf-8")

        print("\nEMAIL BODY:\n")
        email = body

        break
    