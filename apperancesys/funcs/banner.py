from base.exceptions import default_exception, Error500, Error404
from apperancesys.models import Banner


@default_exception(Error500)
def get_banner(count):
    # type: (int) -> list(Banner)
    try:
        photos = Banner.objects.filter(in_use=True).order_by('-id')[:3]
        return photos
    except Banner.DoesNotExist:
        raise Error404("No banner")
