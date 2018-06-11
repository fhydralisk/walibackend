"""
Phone Validator utility

Created by Hangyu Fan, May 6, 2018

Last modified: May 6, 2018
"""

import random
import uuid
from django.conf import settings
from django.utils.module_loading import import_string
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider


class BasePhoneValidator(object):
    """
    Phone Validator Base class.

    Basic flow: Sends a number to a cell phone and return the number.
    """

    DIGITS_VALIDATE = 6

    def generate_and_send(self, pn):
        raise NotImplementedError

    def base_generator(self):
        return "".join(map(lambda x: str(random.randint(0, 9)), range(0, self.DIGITS_VALIDATE)))


class ConsolePhoneValidator(BasePhoneValidator):
    """
    A Phone validator for testing, do not really send messages but print console messages instead.
    """

    def generate_and_send(self, pn):
        v = self.base_generator()
        print v
        return v


class DummyPhoneValidator(BasePhoneValidator):
    STATIC_VCODE = "123456"
    """
    A Dummy validator that always send specified same validation code.
    """

    def generate_and_send(self, pn):
        return self.STATIC_VCODE


class AliyunPhoneValidator(BasePhoneValidator):
    REGION = "cn-hangzhou"
    PRODUCT_NAME = "Dysmsapi"
    DOMAIN = "dysmsapi.aliyuncs.com"

    region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

    def __init__(self):
        appid, appkey = self.load_get_sk()
        self.appid = appid
        self.appkey = appkey
        self.acs_client = AcsClient(self.appid, self.appkey, self.REGION)
        self.template_code = settings.ALYSMS_TEMPLATE_CODE
        self.sign_name = settings.ALYSMS_SIGN_NAME

    def load_get_sk(self):
        key_appid = "APP_ID"
        key_appsecret = "APP_SECRET"
        dict_sk = settings.SK_ALISMS
        if key_appid in dict_sk and key_appsecret in dict_sk:
            pass
        else:
            with open(settings.SK_FILE_PATH, 'r') as f:
                tp = f.readlines()[1].strip().split(',')
                dict_sk[key_appid] = tp[0].strip('"')
                dict_sk[key_appsecret] = tp[1].strip('"')

        return dict_sk[key_appid], dict_sk[key_appsecret]

    def generate_and_send(self, pn):
        vcode = self.base_generator()

        smsRequest = SendSmsRequest.SendSmsRequest()
        smsRequest.set_TemplateCode(self.template_code)

        smsRequest.set_TemplateParam('{"code": "%s"}' % vcode)

        smsRequest.set_OutId(uuid.uuid1())

        smsRequest.set_SignName(self.sign_name)

        smsRequest.set_PhoneNumbers(pn)

        smsResponse = self.acs_client.do_action_with_exception(smsRequest)

        if "Message" not in smsResponse or smsResponse["Message"] != "OK":
            raise ValueError("Failed sending sms validation code.")

        return vcode


phone_validator = import_string(settings.PHONE_VALIDATOR)()
