from src.utilize.logger import get_log
from src.services.gmail_service import GmailService


logger = get_log(__name__)


def main():
    logger.info('Data analysis project')


if __name__ == '__main__':
    main()
