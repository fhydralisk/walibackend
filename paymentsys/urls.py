from django.conf.urls import url, include
from views.dummy_payment import DummyPaymentCallbackView


url_patterns_dummy = [
    url(r'^callback/', DummyPaymentCallbackView.as_view())
]


url_patterns = [
    url(r'^dummy/', include(url_patterns_dummy))
]
