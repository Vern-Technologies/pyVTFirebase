import httpx
import json


def setup(config):
    return Connection(config)


class Connection:

    def __init__(self, config):
        self.api_key = config["apiKey"]

    def auth(self):
        return Auth(self.api_key)


class Auth:
    """ Authentication and User Management Service """

    def __init__(self, api_key):
        self.api_key = api_key
        self.user = None
        self.base_url = 'https://identitytoolkit.googleapis.com/v1/accounts:'
        self.header = {"Content-Type": "application/json; charset=UTF-8"}

    def signIn_with_email_and_password(self, email: str, password: str):
        url = self.base_url + 'signInWithPassword'
        params = {'key': self.api_key}
        data = {"email": email, "password": password, "returnSecureToken": True}
        req = httpx.post(url=url, headers=self.header, params=params, json=data, timeout=3)
        self.user = req.json()
        return req

    def send_password_reset_email(self, email: str = None):
        if email is None:
            email = self.user['email']

        url = self.base_url + 'sendOobCode'
        params = {'key': self.api_key}
        data = {"requestType": "PASSWORD_RESET", "email": email}
        req = httpx.post(url=url, headers=self.header, params=params, json=data, timeout=3)
        return req

    def send_email_verification(self, idToken: str = None):
        if idToken is None:
            idToken = self.user['idToken']

        url = self.base_url + 'sendOobCode'
        params = {'key': self.api_key}
        data = {"requestType": "VERIFY_EMAIL", "idToken": idToken}
        req = httpx.post(url=url, headers=self.header, params=params, json=data, timeout=3)
        return req
