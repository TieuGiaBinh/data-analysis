from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from src.utilize.logger import get_log


logger = get_log(__name__)


# Required Google API scope for reading Gmail messages in read-only mode.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailService:
    # Initializes a Gmail API client using OAuth 2.0 credentials.
    def __init__(self, client_id, client_secret, refresh_token):
        # Create OAuth2 credentials from the provided client ID, secret, and refresh token.
        credentials = Credentials(
          token=None,
          refresh_token=refresh_token,
          token_uri='https://oauth2.googleapis.com/token',
          client_id=client_id,
          client_secret=client_secret,
          scopes=SCOPES,
        )

        # Refresh the access token before making API calls.
        credentials.refresh(Request())

        # Build the Gmail API service instance for version v1.
        self.service = build('gmail', 'v1', credentials=credentials, cache_discovery=False)


    def get_email(self, key_word: str) -> list:
        response = (self.service.users().messages().list(
                        userId='me',
                        q='subject="TCBS - "'
                            ).execute()
                   )
        gmail_ids = [gmail['id'] for gmail in response['message']]
        logger.info(gmail_ids)
        return gmail_ids
