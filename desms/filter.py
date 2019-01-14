import re

from desms.constants import FILTER_REGEX, BLOCK_PHONE_NUMBER_LISTS


def contains_filter_keywords(text):
    """是否包含过滤关键词"""
    regex = FILTER_REGEX
    return re.search(regex, text)


def in_black_number_lists(number):
    """是否在号码黑名单里"""
    if number in BLOCK_PHONE_NUMBER_LISTS:
        return True
    return False


def is_need_filter(number, text):
    if contains_filter_keywords(text) or in_black_number_lists(number):
        return True
    return False
