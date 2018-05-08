"""

"""


class RegistrationSessionKeys(object):
    CACHE_DURATION = 300
    PHONE_NUMBER = "phone_number"
    VALIDATE_STATUS = "validate_status"
    VCODE = "vcode"
    VCODE_LAST_TIME = "vcode_last_time"
    SID = "sid"
    PN_2_SID = "reg_pn_%s"


class ValidateStatus(object):
    VALIDATE_SENT = 1
    VALIDATE_FAILED = 2
    VALIDATE_SUCCEEDED = 3
    MIN_INTERVAL = 60
