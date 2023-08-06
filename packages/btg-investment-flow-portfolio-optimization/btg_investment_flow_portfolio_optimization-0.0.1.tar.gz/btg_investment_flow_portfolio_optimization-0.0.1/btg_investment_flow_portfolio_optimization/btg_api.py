import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util import Retry
import time


class RequestHandler:
    @staticmethod
    def handle_request_exception(e):
        # Define exception handling logic here
        print(f"An error occurred: {str(e)}")
        raise

    @staticmethod
    def check_response_status(response):
        try:
            response.raise_for_status()
        except Exception as e:
            print(f"An error occurred while making a request: {str(e)}")
            raise


class BTGApiHandler:
    def __init__(self, base_url, client_id, client_secret):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = self.create_session()
        self.token_expiration = 0
        self.access_token = None

    def create_session(self):
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.1,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def get_access_token(self):
        current_time = time.time()
        if self.access_token and current_time < self.token_expiration:
            return self.access_token
        else:
            authentication_path = "/cm/authentication/token"
            api_url = f"{self.base_url}{authentication_path}"
            try:
                response = self.session.post(
                    api_url,
                    data={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "grant_type": "client_credentials",
                    },
                    timeout=10,
                )
                RequestHandler.check_response_status(response)
                token_response = response.json()
                self.access_token = token_response["access_token"]
                # assumes that token_response includes 'expires_in' in seconds
                self.token_expiration = current_time + token_response["expires_in"]
                return self.access_token
            except RequestException as e:
                RequestHandler.handle_request_exception(e)

    def get_account_balance(self, account_id):
        method_path = f"/cm/account/{account_id}/balance"
        api_url = f"{self.base_url}{method_path}"
        try:
            response = self.session.get(
                api_url,
                headers={"Authorization": f"Bearer {self.get_access_token()}"},
                timeout=10,
            )
            RequestHandler.check_response_status(response)
            response_body = response.json()["body"]
            return {
                "search_date": response_body["searchDate"],
                "account": response_body["account"],
                "account_id": response_body["accountId"],
                "balance": round(response_body["balance"] / 100, 2),
                "available_balance": round(response_body["availableBalance"] / 100, 2),
                "blocked_amount": response_body["blockedAmount"],
            }
        except RequestException as e:
            RequestHandler.handle_request_exception(e)
