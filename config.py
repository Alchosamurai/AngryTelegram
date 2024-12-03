import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = str(os.environ.get('TELEGRAM_TOKEN'))
SERVER_ADRESS = os.environ.get('SERVER_ADRESS')
API_KEY = os.environ.get('API_KEY')
csrftoken=os.environ.get('csrftoken')