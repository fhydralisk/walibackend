from base.util.db import LastLineConfigManager
from pushsys.models import JPushSecret


class JPSecretManager(LastLineConfigManager):

    CLZ_MODEL = JPushSecret

    @staticmethod
    def extra_filter(qs):
        return qs
