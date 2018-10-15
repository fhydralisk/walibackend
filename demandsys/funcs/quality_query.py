# coding=utf-8

from base.exceptions import WLException
from demandsys.models import ProductTypeL3


MAP_P1NAME_ID = {
    u"PET": 1,
    u"废纸": 2,
    u"废钢": 3,
    u"国产塑料": 4,
    u"有色金属": 5,
}


def get_quality_template_tricky(id, pid):
    # type: (int, ProductTypeL3) -> str
    # FIXME: This is tricky and must be fixed.

    if id is not None:
        return "product_quality_%d.html" % id

    if pid is not None:
        try:
            return "product_quality_%d.html" % MAP_P1NAME_ID[pid.t2id.t1id.tname1]
        except KeyError:
            raise WLException(404, "Cannot locate id of pid.")
