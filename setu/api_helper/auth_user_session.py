from typing import Optional
import logging
from requests import Session, Response


class UserSession(Session):
    """
    Class object containing an API session and auth service API clients and helpers
    """

    def __init__(
            self, username: str = None, password: str = None, gateway_url="https://setu.com"):
        """
        Makes a POST /auth/v1/sessions/current of the auth service

        :param username: (optional) user username to login with
        :param password: (optional) user password to login with
        :param gateway_url: (optional) used to pass in a url instead of using the environments resource file
        """

        super(UserSession, self).__init__()
        self.username = username
        self.password = password

        self.session_id = None
        self.login_response = None
        self.gateway_url = gateway_url
        # Call login
        self.login()

    def login(self, username: str = None, password: str = None):
        """
        Calls the auth login API and stores the session info for further requests
        """
        login_url = f'{self.gateway_url}/auth/sessions'
        if username is None:
            username = self.username
        if password is None:
            password = self.password
        data = {
            'username': username,
            'password': password
        }
        response = self.post(url=login_url, headers=self.headers, json=data)
        show_response = f'Login response: {response.status_code}: {response.text}\n{response.headers}'
        logging.debug(show_response)
        if not response.ok:
            raise LoginException(
                f'Problem logging in as user {username}.\n'
                f'{logging.info(response)}')
        session_id = response.cookies.get('SESSION')
        if not session_id:
            raise LoginException(
                f'Did not receive a session cookie from login call.\n'
                f'Response Headers: {response.headers}\n',
                f'Response Cookies: {response.cookies}\n'
                f'{logging.debug(response)}')
        csrf_token = response.headers.get('X-CSRF-Token')
        if not csrf_token:
            raise LoginException(
                f'Did not receive a CSRF token from login call.\n'
                f'Response Headers: {response.headers}\n',
                f'Response Cookies: {response.cookies}\n'
                f'{logging.debug(response)}')

        # Store the session headers
        self.headers['X-CSRF-Token'] = csrf_token
        self.headers['Cookie'] = 'SESSION={}'.format(session_id)
        self.session_id = session_id
        self.login_response = response


class LoginException(Exception):
    """
    Custom Exception for login failures
    """
