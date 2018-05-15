"""
Pages utility

Written by Hydra, May 15, 2018
"""


def get_page_info(queryset, count_per_page, page, page_start=0):
    """

    :param queryset: The queryset object
    :param count_per_page:
    :param page: current page
    :return: lower_bound, upper_bound, n_pages
    :raise IndexError, if page exceeds max page.
    """

    n_pages = queryset.count() + (count_per_page - 1) / count_per_page
    if page - page_start > n_pages or page - page_start < 0:
        raise IndexError("page out of range")

    start = page * count_per_page - page_start
    end = (page + 1) * count_per_page - page_start
    return start, end, n_pages
