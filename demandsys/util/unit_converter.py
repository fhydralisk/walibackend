"""
Unit converter utilities
"""
from demandsys.model_choices.demand_enum import unit_choice

Number = (int, float, long)


class UnitMetric(object):

    SCALE = {
        unit_choice.T: 1000,
        unit_choice.KG: 1,
    }

    VERBOSE = {
        unit_choice.T: "T",
        unit_choice.KG: "KG",
    }

    def __init__(self, quantity, unit):
        if unit not in unit_choice.get_choices():
            raise ValueError("Invalid unit")

        if not isinstance(quantity, Number):
            raise TypeError("Invalid quantity")

        self._unit = unit
        self._quantity = float(quantity)

    @property
    def quantity(self):
        return self._quantity

    @property
    def unit(self):
        return self._unit

    def scaled_value(self):
        raise NotImplementedError

    @staticmethod
    def from_scaled_value(value, unit):
        return UnitMetric(float(value) / UnitMetric.SCALE[unit], unit)

    def __cmp__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Cannot compare with %s." % str(other.__class__))
        return self.scaled_value() - other.scaled_value()

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __hash__(self):
        return hash((self._unit, self._quantity))

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return UnitMetric.from_scaled_value(self.scaled_value() + other.scaled_value(), self._unit)
        else:
            raise TypeError("Cannot operate with %s." % str(other.__class__))

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return UnitMetric.from_scaled_value(self.scaled_value() - other.scaled_value(), self._unit)
        else:
            raise TypeError("Cannot operate with %s." % str(other.__class__))

    def __mul__(self, other):
        if isinstance(other, Number):
            return UnitMetric(self._quantity * other, self._unit)
        elif (isinstance(other, UnitPriceMetric) and isinstance(self, UnitQuantityMetric))\
                or (isinstance(self, UnitPriceMetric) and isinstance(other, UnitQuantityMetric)):
            # Self is price, other is quantity
            return self.scaled_value() * other.scaled_value()
        else:
            raise TypeError("Cannot operate with %s" % str(other.__class__))

    def __unicode__(self):
        return "%f %s" % (self._quantity, self.VERBOSE[self._unit])


class UnitPriceMetric(UnitMetric):
    def scaled_value(self):
        return self._quantity / self.SCALE[self._unit]


class UnitQuantityMetric(UnitMetric):
    def scaled_value(self):
        return self._quantity * self.SCALE[self._unit]
