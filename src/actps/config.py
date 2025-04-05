import os

from dotenv import load_dotenv


load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
TEST_POSTGRES_URL = os.getenv("TEST_POSTGRES_URL")
POSTGRES_URL_ALEMBIC = os.getenv("POSTGRES_URL_ALEMBIC")
FRONT_URL = os.getenv("FRONT_URL", "")
DOMAIN_BLOCK_LIST_FILE_PATH = os.getenv("DOMAIN_BLOCK_LIST_FILE_PATH")
IP_BLOCK_LIST_FILE_PATH = os.getenv("IP_BLOCK_LIST_FILE_PATH")
REDIS_URL = os.getenv("REDIS_URL")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
