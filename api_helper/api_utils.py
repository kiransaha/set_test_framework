
#!/usr/bin/python


import logging

from setu.api_helper.auth_user_session import UserSession


class SetuUtills:
    def __init__(self, **kwargs):
        self.base_url = "https://setu.com"

    def add_expense(self, user_id, amount):
        session = UserSession()
        add_expense_url = "{0}/add_expense".format(
            self.base_url, )

        payload = {"user_id": user_id, "expense_amount": amount}
        logging.info(f"baseurl {add_expense_url} payload {payload}")
        response = session.post(add_expense_url, json=payload)
        if response.status_code == 200:
            return response.content
        else:
            raise f"api failed with {response.status_code} and error {response.content}"

    def get_user(self, user_number):
        session = UserSession()
        get_user_url = "{0}/get_user?{1}".format(
            self.base_url, user_number)
        logging.info(f"baseurl {get_user_url}")
        response = session.get(get_user_url)
        if response.status_code == 200:
            return response.content
        else:
            raise f"api failed with {response.status_code} and error {response.content}"

    def get_expense(self, user_id):
        session = UserSession()
        get_expense_url = "{0}/get_expense?{1}".format(
            self.base_url, user_id)
        logging.info(f"baseurl {get_expense_url}")
        response = session.post(get_expense_url)
        if response.status_code == 200:
            return response.content
        else:
            raise f"api failed with {response.status_code} and error {response.content}"

    def validate(self, expected, actual):
        assert expected == actual, f"expected was {expected} but got {actual}"
