import logging

from app.db.call_db import call_db


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("call db before")
    call_db()
    logger.info("call db after")


if __name__ == "__main__":
    main()
