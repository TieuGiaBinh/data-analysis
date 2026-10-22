from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailService:
    def __init__(self, client_id, client_secret, refresh_token):
        credentials = Credentials(
          token=None,
          refresh_token=refresh_token,
          token_uri='https://oauth2.googleapis.com/token',
          client_id=client_id,
          client_secret=client_secret,
          scopes=SCOPES,
        )

        credentials.refresh(Request())

        self.service = build('gmail', 'v1', credentials=credentials, cache_discovery=False)
