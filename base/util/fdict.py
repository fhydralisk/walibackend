"""
Fdict importer
"""

import json
from coresys.models import CoreAddressArea, CoreAddressCity, CoreAddressProvince


def address_fdict_importer(jsonpath):
    with open(jsonpath, 'r') as f:
        fdict = json.load(f)
        CoreAddressProvince.objects.all().update(in_use=False)
        CoreAddressCity.objects.all().update(in_use=False)
        CoreAddressArea.objects.all().update(in_use=False)

        for dict_province in fdict:
            pid = dict_province["code"]
            CoreAddressProvince.objects.update_or_create(defaults={
                "province": dict_province["name"],
                "in_use": True
            }, id=pid)

            cities = dict_province.get("sub", [])
            for dict_city in cities:
                cid = dict_city["code"]
                CoreAddressCity.objects.update_or_create(
                    defaults={
                        "pid_id": pid, "city": dict_city["name"], "in_use": True
                    },
                    id=cid)

                areas = dict_city.get("sub", [])
                for dict_area in areas:
                    CoreAddressArea.objects.update_or_create(
                        defaults={
                            "cid_id": cid, "area": dict_area["name"], "in_use": True
                        },
                        id=dict_area["code"]
                    )
