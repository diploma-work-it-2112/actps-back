import os

from dotenv import load_dotenv


load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
TEST_POSTGRES_URL = os.getenv("TEST_POSTGRES_URL")
POSTGRES_URL_ALEMBIC = os.getenv("POSTGRES_URL_ALEMBIC")
FRONT_URL = os.getenv("FRONT_URL", "")
