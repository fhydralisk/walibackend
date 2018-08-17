from django.core.files.base import ContentFile
from django.db.models import Q
from django.db import transaction
from base.exceptions import Error500, default_exception
from usersys.funcs.utils.usersid import user_from_sid
from usersys.model_choices.user_enum import role_choice
from invitesys.models import InviteContractTemplate, InviteContractSign
from invitesys.model_choices.contract_enum import sign_status_choice
from invitesys.model_choices.invite_enum import i_status_choice
from ordersys.funcs.operate_order import create_order as create_order_func
from invitesys.funcs.placeholder2exceptions import get_placeholder2exception


def create_contract(iv_obj, template):
    """
    Create a contract using invite object and save it into a file.
    :param iv_obj: invite object
    :param template: template object
    :return: None?
    """

    def replace_fields(cnt, i_obj):
        # TODO: Get objects from iv_obj
        return cnt

    # Load contract file of template
    # TODO: Cache the template file if possible
    template.path.open()
    content = template.path.read()
    template.path.close()

    # Replace the fields
    content = replace_fields(content, iv_obj)

    # Create and save the file and append correlated field of iv_obj
    try:
        contract = InviteContractSign.objects.get(
            ivid=iv_obj,
            sign_status_A=sign_status_choice.NOT_SIGNED,
            sign_status_B=sign_status_choice.NOT_SIGNED
        )
    except InviteContractSign.DoesNotExist:
        contract = InviteContractSign(
            ivid=iv_obj,
            sign_status_A=sign_status_choice.NOT_SIGNED,
            sign_status_B=sign_status_choice.NOT_SIGNED
        )

    contract.ctid = template
    contract.path.save("contract.html", ContentFile(content))


def get_current_template():
    return InviteContractTemplate.objects.filter(in_use=True).first()


def get_contract_obj(user, cid):
    try:
        contract = InviteContractSign.objects.select_related("ivid", "ivid__uid_s", "ivid__uid_t").get(Q(ivid__uid_s=user) | Q(ivid__uid_t=user), id=cid)
    except InviteContractSign.DoesNotExist:
        raise get_placeholder2exception("invite/contract/ : no such contract in function get_contract_obj")

    return contract


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("invite/contract/content/ : user_sid error"))
def obtain_contract_content(user, cid):

    contract = get_contract_obj(user, cid)
    return contract.content


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("invite/contract/info/ : user_sid error"))
def retrieve_contract_info(user, cid):
    return get_contract_obj(user, cid)


@default_exception(Error500)
@user_from_sid(get_placeholder2exception("invite/contract/sign/ : user_sid error"))
def sign_contract(user, cid, sign_method):
    contract = get_contract_obj(user, cid)

    sign_status_party = {"sign_status_A", "sign_status_B"}

    # FIXME: Status A is buyer or inviter ?
    # if user == contract.ivid.uid_s:
    #     sign = "sign_status_A"
    # elif user == contract.ivid.uid_t:
    #     sign = "sign_status_B"
    # else:
    #     raise AssertionError("user is not A or B")

    # Another Logic
    if user.role == role_choice.BUYER:
        sign = "sign_status_A"
    elif user.role == role_choice.SELLER:
        sign = "sign_status_B"
    else:
        raise AssertionError("user is not A or B")

    assert(contract.ivid.uid_t.role != contract.ivid.uid_s.role)

    # Check invite status
    if contract.ivid.i_status != i_status_choice.CONFIRMED:
        raise get_placeholder2exception("invite/contract/sign/ : cannot change sign status")

    # FIXME: If already signed or rejected, cannot revert?
    if getattr(contract, sign) != sign_status_choice.NOT_SIGNED:
        raise get_placeholder2exception("invite/contract/sign/ : already signed or rejected")

    setattr(contract, sign, sign_method)

    # Check invite status and test if should create order.

    create_order = False

    if contract.sign_status_A == sign_status_choice.ACCEPTED and contract.sign_status_B == sign_status_choice.ACCEPTED:
        contract.ivid.i_status = i_status_choice.SIGNED
        create_order = True

    if sign_method == sign_status_choice.REJECTED:
        contract.ivid.i_status = i_status_choice.CONTRACT_NOT_AGREE
        # print ("not agree")

    with transaction.atomic():
        contract.ivid.save()
        contract.save()
        if create_order:
            # TODO: Log
            create_order_func(user, contract.ivid)

    return contract




