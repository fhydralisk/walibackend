from demandsys.models import ProductTypeL1, ProductTypeL2, ProductTypeL3, ProductQuality, ProductWaterContent
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


@default_exception(Error500)
def get_l3(t2id):
    """
    
    :param t2id: 
    :return: 
    """
    return ProductTypeL3.objects.filter(in_use=True, t2id=t2id)


@default_exception(Error500)
def get_l3_quality(t3id):
    """
    
    :param t3id: 
    :return: 
    """
    return ProductQuality.objects.filter(in_use=True, t3id=t3id)


@default_exception(Error500)
def get_l1_2_3():
    """
    
    :return: 
    """
    return ProductTypeL1.objects.filter(in_user=True)


@default_exception(Error500)
def get_water_content():
    """
    
    :return: 
    """
    return ProductWaterContent.objects.filter(in_use=True)









