"""
Database utilities
"""


def update_instance_from_dict(instance, dic, save=False):
    for k, v in dic.items():
        if hasattr(instance, k):
            if isinstance(v, dict):
                update_instance_from_dict(getattr(instance, k), v, save)
            else:
                setattr(instance, k, v)

    if save:
        instance.save()
