from rest_framework.views import APIView
from django.shortcuts import render
from base.views import WLAPIView


class QualityView(WLAPIView, APIView):

    def get(self, request):
        return render(request, template_name='product_quality.html')

