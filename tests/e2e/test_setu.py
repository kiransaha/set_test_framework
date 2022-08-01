#!/usr/bin/python


import pytest
from api_helper.api_utils import SetuUtills


class TestSensorInstallviaUserData:

    @pytest.mark.parametrize('params',
                             [{'user_num': '1234567890', 'expense_amount': '100000000'},
                              {'user_num': '1234567890', 'expense_amount': '0'},
                              {'user_num': '9012345678', 'expense_amount': '11'},
                              {'user_num': '9012345678', 'expense_amount': '-11'}
                              ],
                             ids=['expense_amount_100000000', 'expense_amount_0', 'expense_amount_11',
                                  'expense_amount_11_negative'])
    def test_validate_expense(self, params):
        """
        Validate expense addition
        STEPS:- 1. getting the preexisting expense amount of the user
                2. Adding expense to the user
                3. Validating by again getting the expense amount after addition
                4. Then matching it with preexisting value that we got in step 1 + expense amount
        """

        try:
            setu_utills = SetuUtills()
            user_id = setu_utills.get_user(params.get('user_num'))
            before_expense = setu_utills.get_expense(user_id=user_id)
            setu_utills.add_expense(user_id=user_id,amount=params.get("expense_amount"))
            after_expense = setu_utills.get_expense(user_id=user_id)
            setu_utills.validate(before_expense+params.get("expense_amount"), after_expense)

        finally:
            # Cleanup Actions
            pass
