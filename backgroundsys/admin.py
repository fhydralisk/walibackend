from .admin_site import admin_site
from model_admin import core_admin, user_admin, simplified_invite_admin, push_admin, demand_admin, appraisal_admin

managed = [
    core_admin,
    user_admin,
    push_admin,
    simplified_invite_admin,
    demand_admin,
    appraisal_admin,
]


def register_all():
    for m in managed:
        if hasattr(m, 'to_register'):
            for r in m.to_register:
                admin_site.register(*r)


register_all()
