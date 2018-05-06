"""
Phone Validator utility

Created by Hangyu Fan, May 6, 2018

Last modified: May 6, 2018
"""

import random
from django.core.cache import cache

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



