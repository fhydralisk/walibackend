from usersys.model_choices.user_enum import role_choice
from demandsys.model_choices.demand_enum import t_demand_choice


class _TDemandTranslator(object):

    MAP_ROLE_DEMAND = {
        role_choice.SELLER: t_demand_choice.SELL,
        role_choice.BUYER: t_demand_choice.BUY,
    }

    MAP_DEMAND_ROLE = {
        t_demand_choice.SELL: role_choice.SELLER,
        t_demand_choice.BUY: role_choice.BUYER,
    }

    def from_role(self, role):
        """
        role -> t_demand
        :param role:
        :return:
        """

        return self.MAP_ROLE_DEMAND[role]

    def from_t_demand(self, t_demand):
        """
        t_demand -> role
        :param t_demand:
        :return:
        """

        return self.MAP_DEMAND_ROLE[t_demand]


t_demand_translator = _TDemandTranslator()
