"""
Pages utility

Written by Hydra, May 15, 2018
"""


def get_page_info(queryset, count_per_page, page, page_start=0, index_error_excepiton=None):
    """

    :param queryset: The queryset object
    :param count_per_page:
    :param page: current page
    :param page_start,
    :param index_error_excepiton
    :return: lower_bound, upper_bound, n_pages
    :raise IndexError, if page exceeds max page or index_error_exception.
    """

    n_pages = (queryset.count() + (count_per_page - 1)) / count_per_page
    if (page - page_start > n_pages - 1 or page - page_start < 0) and not page == page_start:
        if index_error_excepiton is not None:
            raise index_error_excepiton
        else:
            raise IndexError("page out of range")

    start = page * count_per_page - page_start
    end = (page + 1) * count_per_page - page_start
    return start, end, n_pages


def get_page_info_list(o_list, count_per_page, page, page_start=0, index_error_excepiton=None):
    """

    :param o_list: The list object
    :param count_per_page:
    :param page: current page
    :param page_start,
    :param index_error_excepiton
    :return: lower_bound, upper_bound, n_pages
    :raise IndexError, if page exceeds max page or index_error_exception.
    """

    n_pages = (len(o_list) + (count_per_page - 1)) / count_per_page
    if (page - page_start > n_pages - 1 or page - page_start < 0) and not page == page_start:
        if index_error_excepiton is not None:
            raise index_error_excepiton
        else:
            raise IndexError("page out of range")

    start = page * count_per_page - page_start
    end = (page + 1) * count_per_page - page_start
    return start, end, n_pages
