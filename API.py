import requests
import config
import io
import json

class API:
    _URL = config.SERVER_ADRESS
    _headers = {
        'Cookie': f"csrftoken={config.csrftoken}"
    }

    @classmethod
    def merge_telegram(cls, data):
        data['api_key'] = str(config.API_KEY)  
        print(data)
        response = requests.post(f'{cls._URL}/api/merge-telegram', json=data, headers=cls._headers)
        return response.status_code
        
    @classmethod
    def merge_phone(cls, data):
        data['api_key'] = str(config.API_KEY)
        response = requests.post(f'{cls._URL}/api/merge-phone', json=data, headers=cls._headers)
        return response.status_code
    
