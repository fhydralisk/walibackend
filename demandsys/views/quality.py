from django.template.loader import render_to_string
from rest_framework.views import APIView
from base.views import WLAPIView
from demandsys.serializers.quality_api import QualityQuerySerializer
from demandsys.funcs.quality_query import get_quality_template_tricky


class QualityView(WLAPIView, APIView):

    def get(self, request):
        data, context = self.get_request_obj(request)

        seri = QualityQuerySerializer(data=data)
        self.validate_serializer(seri)

        template_name = get_quality_template_tricky(**seri.validated_data)

        return self.generate_response(
            data={
                "content": render_to_string(template_name=template_name)
            },
            context=context
        )

