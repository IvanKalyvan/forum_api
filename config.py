import os

from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_DATABASE")
test_db_database = os.getenv("TEST_DB_DATABASE")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

sender_email = os.getenv("SENDER_EMAIL")
email_app_password = os.getenv("EMAIL_APP_PASSWORD")

openai_key = os.getenv("OPENAI_API_KEY")
openai_organization = os.getenv("OPENAI_API_ORGANIZATION")

url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
test_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{test_db_database}"