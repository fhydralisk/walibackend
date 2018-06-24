from base.exceptions import default_exception, Error500, Error404
from apperancesys.models import Banner


@default_exception(Error500)
def get_banner():
    # type: (int) -> Banner
    try:
        photo = Banner.objects.last()
        return photo
    except Banner.DoesNotExist:
        raise Error404("No banner")
