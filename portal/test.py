from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'P:/Projects/acewebsite-v2/creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    creds = Credentials(token='ya29.GlxvB8afBhlM_FWAQLfN-R2Z2Uratp4goR3746ZsfRIAwsGq836HFkNjapPf4weEc45MSplSl7euLWgrh6juPHkcf-5b0Z0MTqeHyY6-txcyt_ZKym8e9G0tH5FCew')
    print(creds._id_token);

    service = build('drive', 'v3', credentials=creds)

    media_body = MediaFileUpload(filename='P:/Downloads/[HorribleSubs]_Dororo_-_13_[720p].mp4-720.mp4', chunksize=1024 * 1024 * 50, resumable=True)

    meta = {
        "name": "TestFile.mkv",
        "parents": ["1-s27OYxO9-IZfQMBzodR9h1ezfPK8ZU8"]
    }

    file = service.files().create(body=meta, media_body=media_body).execute()

    print(file, file.get("id"))

if __name__ == '__main__':
    main()