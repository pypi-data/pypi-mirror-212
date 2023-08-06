from multiprocessing.sharedctypes import Value
import requests

class predict(object):
    url = "https://predict7.p.rapidapi.com/"
    
    def __init__(self, api_key=None):
        if not api_key:
            raise ValueError("API key is missing")
        self.api_key = api_key
    
    def predict(self, data, horizon, cls):
        if not data:
            ValueError("Historical data is missing")
        if not horizon:
            ValueError("Horizon is missing")
        if not cls:
            ValueError("Confidence levels are missing")
        
        payload = {
            "data": data,
            "horizon": horizon,
            "cls": cls
        }
        
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Host": "predict7.p.rapidapi.com",
            "X-RapidAPI-Key": self.api_key
        }
        
        response = requests.post(self.url, json=payload, headers=headers)
        return response.json()
