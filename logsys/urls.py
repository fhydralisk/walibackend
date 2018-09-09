from django.conf.urls import include, url
import logsys.views.order_logs as order_logs
import logsys.views.appraisal_logs as appraisal_logs
import logsys.funcs.log_invite

url_patterns_order = [
    url(r'^obtain_order/', order_logs.ObtainLogOrderStatusView.as_view()),
    url(r'^obtain_protocol/', order_logs.ObtainLogOrderProtocolStatusView.as_view()),
]


url_patterns_appraisal = [
    url(r'^log/$', appraisal_logs.ObtainAppraisalLogView.as_view()),
]


url_patterns = [
    url(r'^order/', include(url_patterns_order)),
    url(r'^appraisal/', include(url_patterns_appraisal)),
]
