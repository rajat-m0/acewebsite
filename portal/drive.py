import json
import requests
from django.core.files.storage import default_storage
from celery import shared_task
from django.utils import timezone
from datetime import timedelta, datetime
from settings.models import Setting
# from google.oauth2 import service_account
from django.conf import settings
import os
from ace.celery import celery_app
from django.core.exceptions import ObjectDoesNotExist



from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

try:
    # DRIVE_TOKENS = {
    #     'access' : Setting.objects.get(key_name='drive_access_token').key_val, #'',
    #     'refresh' : Setting.objects.get(key_name='drive_refresh_token').key_val, #'1/WWpT_MbRuQUzkyuU1fzWL40KpoXwJFP1G0qb4yNviPY',
    #     'expires_at' : datetime.strptime(Setting.objects.get(key_name='drive_token_expires').key_val, DATETIME_FORMAT)
    # }

    

    DRIVE_BASE_FOLDER = Setting.objects.get(key_name='drive_base_folder').key_val
except Exception as e:
    DRIVE_BASE_FOLDER = None
    # raise e
    print("Google Drive settings not available in settings table.\nSet them to ensure proper working of drive upload system")
class DriveToken():
    def get(self, name):
        if name == 'access':
            return Setting.objects.get(key_name='drive_access_token').key_val
        elif name == 'refresh':
            return Setting.objects.get(key_name='drive_refresh_token').key_val
        elif name == 'expires_at':
            return datetime.strptime(Setting.objects.get(key_name='drive_token_expires').key_val, DATETIME_FORMAT)
    
    def store(self, name, val):
        if name == 'access':
            return Setting.objects.filter(key_name='drive_access_token').update(key_val=val, updated_at=timezone.now())
        elif name == 'refresh':
            return Setting.objects.filter(key_name='drive_refresh_token').update(key_val=val, updated_at=timezone.now())
        elif name == 'expires_at':
            return Setting.objects.filter(key_name='drive_token_expires').update(key_val=val.strftime(DATETIME_FORMAT), updated_at=timezone.now())

DRIVE_TOKENS = DriveToken()
DRIVE_CLIENT_SECRET = 'nepTTWrJ41xQ63a-N0GctNLM'
DRIVE_CLIENT_ID = '137271572739-030ao68ubk7s3cpfupokeln5j90sao27.apps.googleusercontent.com'


def update_token(response):
    # DRIVE_TOKENS['access'] = response.get('access_token')
    # DRIVE_TOKENS['expires_at'] = timezone.now() + timedelta(seconds=response.get('expires_in'))

    # Setting.objects.filter(key_name='drive_access_token').update(key_val=DRIVE_TOKENS['access'])
    # Setting.objects.filter(key_name='drive_token_expires').update(key_val=DRIVE_TOKENS['expires_at'].strftime(DATETIME_FORMAT))

    DRIVE_TOKENS.store('access', response.get('access_token'))
    DRIVE_TOKENS.store('expires_at', timezone.now() + timedelta(seconds=response.get('expires_in')))

    if response.get('refresh_token', None) is not None:
        DRIVE_TOKENS.store('refresh', response.get('refresh_token'))

        # DRIVE_TOKENS['refresh'] = response.get('access_token', None)

        # Setting.objects.filter(key_name='drive_refresh_token').update(key_val=DRIVE_TOKENS['refresh'])


# refresh_access_token()

def create_folder(name, parent=DRIVE_BASE_FOLDER, description=None):
    headers = {"Authorization": "Bearer {}".format(DRIVE_TOKENS.get('access'))}
    para = {
        "name": name,
        "mimeType" : "application/vnd.google-apps.folder",
        # "parents": ["1QkyM4_Tk_XZXN0S4lMT1fBkx5dF6_U8I"]
    }
    if parent is not None:
        para['parents'] = parent if isinstance(parent, list) else [parent]

    if description is not None:
        para['description'] = str(description)
    
    
    r = requests.post(
        "https://www.googleapis.com/drive/v3/files",
        headers=headers,
        json=para
    )

    response = json.loads(r.text)
    
    if response.get('error', None) is not None:
        print("Exception while creating folder", response.get('error'))
        raise Exception(response.get('error'))
    
    return response.get('id')

    

# @shared_task(serializer='pickle')
def upload_drive_task_old(filename, tmp_storage_file, submission_obj, parent):
    print(filename, tmp_storage_file, submission_obj, parent)

    headers = {"Authorization": "Bearer {}".format(DRIVE_TOKENS.get('access'))}
    para = {
        "name": filename,
        "parents": [parent]
    }

    with default_storage.open(tmp_storage_file) as file:
    
        files = {
            'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
            # 'file': open(os.path.join(settings.BASE_DIR, 'portalapp/sample.png'), "rb")
            'file': file
        }

        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
        )

    response = json.loads(r.text)
    url = 'https://drive.google.com/file/d/{}/view'.format(response['id'])

    
    default_storage.delete(tmp_storage_file)
    # submission_obj = Submission.objects.get(id=submission_id)
    submission_obj.submission_url = url
    submission_obj.task_submitted = True
    submission_obj.save()


def upload_drive_task(filename, tmp_storage_file, submission_obj, parent):
    print(filename, tmp_storage_file, submission_obj, parent)

    meta = {
        "name": filename,
        "parents": [parent]
    }

    file_path = default_storage.path(tmp_storage_file)

    print(file_path)

    try:
        creds = Credentials(token=DRIVE_TOKENS.get('access'))
        service = build('drive', 'v3', credentials=creds)
        media_body = MediaFileUpload(filename=file_path, chunksize=1024*1024*50, resumable=True)

        file = service.files().create(body=meta, media_body=media_body).execute()
    except RefreshError:
        refresh_token()

        creds = Credentials(token=DRIVE_TOKENS.get('access'))
        service = build('drive', 'v3', credentials=creds)
        media_body = MediaFileUpload(filename=file_path, chunksize=1024*1024*50, resumable=True)

        file = service.files().create(body=meta, media_body=media_body).execute()

    url = 'https://drive.google.com/file/d/{}/view'.format(file.get('id'))

    # submission_obj = Submission.objects.get(id=submission_id)
    submission_obj.submission_url = url
    submission_obj.task_submitted = True
    submission_obj.save()

    if not media_body._fd.closed:
        media_body._fd.close()
    
    default_storage.delete(tmp_storage_file)


# @shared_task(serializer='pickle', max_retries=None, default_retry_delay=3000, bind=True)
def refresh_token():
    print('refreshing token')

    data = {
        'client_secret' : DRIVE_CLIENT_SECRET,
        'grant_type' : 'refresh_token',
        'refresh_token' : DRIVE_TOKENS.get('refresh'),
        'client_id' : DRIVE_CLIENT_ID
    }
    r = requests.post(
        "https://www.googleapis.com/oauth2/v4/token",
        data = data
    )

    response = json.loads(r.text)
    print(response)
    update_token(response)

    # try:
    #     self.retry(countdown=3000)
    # except:
    #     print("Retry Exception")
'''
    SCOPES = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.appdata',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive.metadata',
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive.photos.readonly',
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/drive.scripts'
    ]

    SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'service-account.json')

    print(SERVICE_ACCOUNT_FILE)

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    delegated_credentials = credentials.with_subject('csi-sb-ace@vips.edu')

    headers = {}
    print(credentials.valid)

    print(credentials.apply(headers))

    print(headers)'''
