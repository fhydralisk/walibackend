from .admin_site import admin_site
from model_admin import core_admin, order_admin, user_admin


managed = [
    core_admin,
    order_admin,
    user_admin,
]


def register_all():
    for m in managed:
        if hasattr(m, 'to_register'):
            for r in m.to_register:
                admin_site.register(*r)


register_all()
