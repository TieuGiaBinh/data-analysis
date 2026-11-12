from pathlib import Path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from src.utilize.logger import get_log


# Required Google API scope for reading Gmail messages in read-only mode.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

logger = get_log(__name__)


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
        self.service = build(
            'gmail',
            'v1',
            credentials=credentials,
            cache_discovery=False,
        )

    def get_email_ids(self, key_word: str) -> list:
        # Search Gmail messages whose subject contains the provided keyword.
        # The Gmail API supports Gmail query syntax, so we filter by subject:
        # `subject:<keyword>`.
        response = (
            self.service.users()
            .messages()
            .list(userId='me', q=f'subject:{key_word}')
            .execute()
        )

        # Extract each message ID from the API response.
        # If no messages match the search, `messages` may be missing,
        # so we use `.get(..., [])` to avoid a KeyError.
        gmail_ids = [gmail['id'] for gmail in response.get('messages', [])]

        # Return the list of matching Gmail message IDs.
        return gmail_ids

    def get_attachment(self, gmail_id: str):
        response = (
            self.service.users()
            .messages()
            .get(userId='me', id=gmail_id, format='full', fields='payload')
            .execute()
        )
        payload = response.get("payload", {})
        parts = payload.get("parts", [])
        for part in parts:
            self._payload_process(gmail_id, part)

    def _payload_process(self, name: str, part: dict):
        filename = part.get('filename', '')
        file_name = f'{name}_{filename}'

        if filename.lower().endswith('.pdf'):
            body = part.get('body', {})
            attachment_id = body.get('attachmentId')

            if attachment_id:
                attachment = (
                    self.service.users()
                    .messages()
                    .attachments()
                    .get(userId='me', id=attachment_id, messageId=name)
                    .execute()
                )
                file_data = attachment.get('data')
                decoded_data = base64.urlsafe_b64decode(file_data)
                path_file = Path(file_name).write_bytes(decoded_data)
                logger.info(f'path file: {path_file}')
            else:
                logger.warning(f'No attachment was found in {filename}')

        for child in part.get('part', []):
            self._payload_process(name, child)
