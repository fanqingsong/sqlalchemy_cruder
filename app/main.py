import logging
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)



from app.call_db import call_db


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("call db before")
    call_db()
    logger.info("call db after")


if __name__ == "__main__":
    main()
