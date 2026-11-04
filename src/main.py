import os
from src.utilize.logger import get_log
from src.services.gmail_service import GmailService


logger = get_log(__name__)


def main():
    logger.info('Data analysis project')
    gmail_service = GmailService(os.environ['GMAIL_CLIENT_ID'], os.environ['GMAIL_CLIENT_SECRET'], os.environ['GMAIL_REFRESH_TOKEN'])
    gmail_ids = gmail_service.get_email_ids('TCBS - ')
    logger.info(gmail_ids)
    for gmail_id in gmail_ids:
        file = gmail_service.get_attachment(gmail_id)
        logger.info(file)


if __name__ == '__main__':
    main()
