import requests
import numpy

class Predictor(object):
    
    url = "https://predict7.p.rapidapi.com/"
    NCL_MAX = 100
    NVALUE_MIN = 5
    NVALUE_MAX = 10000000

    def __init__(self, api_key=None):
        
        if not api_key:
            return ValueError("API key is missing")
        self.api_key = api_key
    
    def predict(self, data, horizon, cls):
        
        # Tests on the data set
    
        if data is None:
            return ValueError("The data set is missing")
        try:
            data = numpy.array(data)
        except Exception as e:
            return ValueError("The data set is not in the right format : " + str(e))
        if not numpy.issubdtype(data.dtype, numpy.number):
            return ValueError("The data set must contain only numeric values")
        if numpy.any(data < 0):
            return ValueError("The data set must not contain negative values")
        if len(data) < self.NVALUE_MIN:
            return ValueError("The data set does not contain enough values")
        if len(data) > self.NVALUE_MAX:
            return ValueError("The data set is too large")
        data = data.tolist()

        # Tests on the projection horizon

        if horizon is None:
            return ValueError("The projection horizon is missing")
        if not isinstance(horizon, int):
            return ValueError("The projection horizon must be an integer")
        try:
            horizon = int(horizon)
        except Exception as e:
            return ValueError("The projection horizon is not in the right format : " + str(e))
        if horizon < 1:
            return ValueError("The projection horizon must be at least 1")


        # Tests on the confidence levels

        if cls is None:
            return ValueError("The confidence levels are missing")
        try:
            cls = numpy.array(cls)
        except Exception as e:
            return ValueError("The confidence levels are not in the right format : " + str(e))
        if not numpy.issubdtype(cls.dtype, numpy.number):
            return ValueError("The confidence levels must be in numeric values")
        if numpy.logical_or(cls < 0, cls > 1).any():
            return ValueError("The confidence levels must be between 0 and 1")
        if len(cls) > self.NCL_MAX:
            return ValueError("The number of confidence levels is too large")

        cls = numpy.unique(cls)
        cls = numpy.sort(cls)
        cls = cls.tolist()
        
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
