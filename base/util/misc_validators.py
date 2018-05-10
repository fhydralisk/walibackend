"""
Regex validator for phone number, email, etc.

Created by Hangyu Fan, May 6, 2018

Last modified: May 7, 2018
"""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

import re
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class AbstractValidator(object):
    message = _('Enter a valid value.')
    code = 'invalid'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def validate(self, vstr):
        raise NotImplementedError

    def __call__(self, value):
        if not self.validate(value):
            raise ValidationError(self.message, code=self.code)


@deconstructible
class RegexAbstractValidator(AbstractValidator):

    REGEX_PATTERN = r''

    def __init__(self, **kwargs):
        if isinstance(self.REGEX_PATTERN, basestring):
            self.reg = re.compile(self.REGEX_PATTERN)
        super(RegexAbstractValidator, self).__init__(**kwargs)

    def regex_validate(self, vstr):
        if not isinstance(vstr, basestring):
            return False

        return self.reg.match(vstr) is not None

    def validate(self, vstr):
        return self.regex_validate(vstr)


@deconstructible
class PNValidator(RegexAbstractValidator):
    REGEX_PATTERN = r'^((13[0-9])|(14[0-9])|(15([0-9]))|(18[0-9]))|(17[0-9])\d{8}$'


@deconstructible
class DummyValidator(AbstractValidator):
    """
    Dummy Validator always pass validations
    """
    def validate(self, vstr):
        return True


class ValidatorManager(object):
    def __init__(self):
        self._validators = {
            e["NAME"]: import_string(e["CLASS"])(**(e["ARGS"] if "ARGS" in e else {}))
            for e in settings.STRING_VALIDATORS
        }

    def validate(self, vstr, vname):
        if vname not in self._validators:
            raise KeyError("validator not exist")
        else:
            return self._validators[vname].validate(vstr)

    def get_validator(self, vname):
        if vname not in self._validators:
            raise KeyError("validator not exist")
        else:
            return self._validators[vname]


validators = ValidatorManager()
