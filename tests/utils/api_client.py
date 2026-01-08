import requests
import json
from logging import Logger
from pydantic import BaseModel

class APIClient:
    def __init__(self, base_url: str, logger: Logger):
        self.base_url = base_url
        self.logger = logger

    def _prepare_data(self, data):
        """
        Converts Pydantic model to dict for JSON serialization.
        If data is already a dict, returns as is.
        """
        if isinstance(data, BaseModel):
            return data.model_dump(mode='json')
        return data

    def _log_request(self, method, url, body=None):
        self.logger.info(f"REQUEST: {method} {url}")
        if body:
            # Pretty print JSON for readability
            self.logger.info(f"PAYLOAD: {json.dumps(body, indent=2)}")

    def _log_response(self, response):
        try:
            # Try to parse JSON for logging
            content = json.dumps(response.json(), indent=2)
        except:
            content = response.text
            
        self.logger.info(f"RESPONSE: {response.status_code} {response.reason}")
        if content:
             self.logger.info(f"BODY: {content}")

    def post(self, endpoint, data=None):
        # Prepare data
        json_data = self._prepare_data(data)
        url = f"{self.base_url}{endpoint}"
        self._log_request("POST", url, json_data)
        
        response = requests.post(url, json=json_data)
        
        self._log_response(response)
        return response

    def get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        self._log_request("GET", url)
        
        response = requests.get(url)
        
        self._log_response(response)
        return response

    def put(self, endpoint, data=None):
        # Prepare data
        json_data = self._prepare_data(data)
        url = f"{self.base_url}{endpoint}"
        self._log_request("PUT", url, json_data)

        response = requests.put(url, json=json_data)
        
        self._log_response(response)
        return response

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        self._log_request("DELETE", url)
        
        response = requests.delete(url)
        
        self._log_response(response)
        return response