# coding=utf-8
from django.shortcuts import render
from coresys.models.address import CoreAddressProvince
from django.http import JsonResponse


def choose_province(request):
    """查询省"""

    provinces = CoreAddressProvince.objects.filter(pid=None)

    p_lists = [{"p_id": province.id, "p_name": province.name} for province in provinces]
    p_info = {"p_lists": p_lists}

    return JsonResponse(p_info, safe=False)
