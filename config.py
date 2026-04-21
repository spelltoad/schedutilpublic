import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set")
