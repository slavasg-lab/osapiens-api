import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv(".env")

Base = declarative_base()

def json_serializer(obj):
    """
    The default JSON serializer in Python's json module.
    """
    return json.dumps(obj)

def json_deserializer(text):
    """
    The default JSON deserializer in Python's json module.
    """
    return json.loads(text)

engine = create_engine(
    os.environ["DATABASE_URL"],
    json_serializer=json_serializer,
    json_deserializer=json_deserializer,
    connect_args={},
    # If using PostgreSQL, the following line can enable the psycopg2 JSONB support:
    # execution_options={"json_serializer": json_serializer, "json_deserializer": json_deserializer},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
