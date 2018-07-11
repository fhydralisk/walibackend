"""
Phone Validator utility

Created by Hangyu Fan, May 6, 2018

Last modified: May 6, 2018
"""

import random
from django.conf import settings
from django.utils.module_loading import import_string


class BasePhoneValidator(object):
    """
    Phone Validator Base class.

    Basic flow: Sends a number to a cell phone and return the number.
    """

    DIGITS_VALIDATE = 6

    def generate_and_send(self, pn):
        raise NotImplementedError

    def base_generator(self):
        return "".join(map(lambda x: str(random.randint(0, 9)), range(0, self.DIGITS_VALIDATE)))


class ConsolePhoneValidator(BasePhoneValidator):
    """
    A Phone validator for testing, do not really send messages but print console messages instead.
    """

    def generate_and_send(self, pn):
        v = self.base_generator()
        print v
        return v


class DummyPhoneValidator(BasePhoneValidator):
    STATIC_VCODE = "123456"
    """
    A Dummy validator that always send specified same validation code.
    """

    def generate_and_send(self, pn):
        return self.STATIC_VCODE


phone_validator = import_string(settings.PHONE_VALIDATOR)()
