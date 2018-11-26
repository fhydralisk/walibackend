import uuid
import logging
import json
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from .validator import BasePhoneValidator
from base.models import PhoneValidatorMasterKey
from base.util.db import LastLineConfigManager


logger = logging.getLogger(__name__)


class MasterKeyManager(LastLineConfigManager):
    cls_logger = logger
    CLZ_MODEL = PhoneValidatorMasterKey

    @staticmethod
    def extra_filter(qs):
        return qs.filter(in_use=True)


class AliyunPhoneValidator(BasePhoneValidator):
    REGION = "cn-hangzhou"
    PRODUCT_NAME = "Dysmsapi"
    DOMAIN = "dysmsapi.aliyuncs.com"

    region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

    def __init__(self):
        self.template_code = None
        self.sign_name = None
        self.acs_client = None

        self.mk_manager = MasterKeyManager(reload_callback=self.change_acs_client)
        # Should not load at start, cause migration failure.
        # self.change_acs_client(self.mk_manager.instance)

    def change_acs_client(self, instance):
        # type: (PhoneValidatorMasterKey) -> None
        if instance is None:
            self.acs_client = None
            self.template_code = None
            self.sign_name = None
        else:
            self.acs_client = AcsClient(instance.app_key, instance.app_secret, self.REGION)
            self.template_code = instance.template_code
            self.sign_name = instance.sign_name.encode('utf-8')

    def generate_and_send(self, pn):
        vcode = self.base_generator()

        # Lazy loading.
        if self.acs_client is None and self.mk_manager.instance is not None:
            self.change_acs_client(self.mk_manager.instance)

        # Check acs client
        if self.acs_client is None:
            logger.warning("AcsClient is None, which leads to failure during sending validation sms!")
        else:
            sms_request = SendSmsRequest.SendSmsRequest()
            sms_request.set_TemplateCode(self.template_code)

            sms_request.set_TemplateParam('{"code": "%s"}' % vcode)

            sms_request.set_OutId(uuid.uuid1())

            sms_request.set_SignName(self.sign_name)

            sms_request.set_PhoneNumbers(pn)

            try:
                sms_response = self.acs_client.do_action_with_exception(sms_request)

                sms_response_json = json.loads(sms_response)

                if "Message" not in sms_response_json or sms_response_json["Message"] != "OK":
                    logger.error("Failed sending sms validation code. ")

            except:
                logger.exception("Error while sending validation sms.")

            return vcode
