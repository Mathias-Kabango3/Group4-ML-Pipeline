from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URI = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:DZ2lPprGVI3Y@ep-cool-surf-a5shclth-pooler.us-east-2.aws.neon.tech/group4?sslmode=require&channel_binding=require')

engine = create_engine(POSTGRES_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()