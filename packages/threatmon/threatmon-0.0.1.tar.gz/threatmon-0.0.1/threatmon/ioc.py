import requests

class IOC_API():
    def __init__(self, api_token = "", limit = 10):
        self.api_token = api_token
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        self.limit = limit
        self.json_data = {
            'api_token': self.api_token,
            'limit': self.limit,
        }

    def daily_ioc(self,):
        response = requests.post('https://ioc.threatmonit.io/api/daily-ioc/', headers=self.headers, json=self.json_data)

        return response
