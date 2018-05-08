"""
Field Choice

Created by Hangyu Fan, May 5, 2018

Last modified: May 5, 2018
"""


class FieldChoice(object):
    """
    Abstract class for describing the enumeration of model fields.
    """

    CHOICE_DISPLAY = (
        ('real_enum_data', 'verbose_name', 'PARAM_NAME'),
    )

    MAX_LENGTH = None

    def __init__(self):
        self.choice = self._build_django_choice()
        param_map = self._build_parameter_name()
        for k, v in param_map.items():
            self.__setattr__(k, v)

        self._choice_values = [v[0] for v in self.CHOICE_DISPLAY]

    def _build_django_choice(self):
        return tuple(map(lambda x: (x[0], x[1]), self.CHOICE_DISPLAY))

    def _build_parameter_name(self):
        return dict(map(lambda x: (x[2], x[0]), self.CHOICE_DISPLAY))

    def validate(self, v):
        return v in self._choice_values
