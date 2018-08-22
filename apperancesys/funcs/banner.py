from base.exceptions import default_exception, Error500
from apperancesys.models import Banner
from base.util.placeholder2exceptions import get_placeholder2exception


@default_exception(Error500)
def get_banner(count):
    # type: (int) -> list(Banner)
    try:
        photos = Banner.objects.filter(in_use=True).order_by('-id')[:3]
        return photos
    except Banner.DoesNotExist:
        raise get_placeholder2exception("appearance/banner/ : no banner in get_banner")
