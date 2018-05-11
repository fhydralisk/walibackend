from demandsys.models import ProductTypeL1, ProductTypeL2, ProductTypeL3
from base.exceptions import default_exception, Error500


@default_exception(Error500)
def get_l1():
    """

    :return:
    """
    return ProductTypeL1.objects.filter(in_user=True)


@default_exception(Error500)
def get_l2(t1id):
    """

    :param t1id: id of Product Type Level 1
    :return: lists of ProductTypeL2 Objects
    """
    return ProductTypeL2.objects.filter(in_use=True, t1id=t1id)
