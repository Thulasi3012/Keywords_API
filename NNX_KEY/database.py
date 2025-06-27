import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# Azure PostgreSQL DB (Transcription DB)
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

TRANSCRIPTION_DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
transcription_engine = create_engine(TRANSCRIPTION_DB_URL)
TranscriptionSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=transcription_engine)

# #  MySQL (Local Comparative DB)
# MYSQL_USER = os.getenv("MYSQL_USER")
# MYSQL_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD"))
# MYSQL_HOST = os.getenv("MYSQL_HOST")
# MYSQL_PORT = os.getenv("MYSQL_PORT")
# MYSQL_DB = os.getenv("MYSQL_DB")

# COMPARATIVE_DB_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
# comparative_engine = create_engine(COMPARATIVE_DB_URL)
# ComparativeSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=comparative_engine)

