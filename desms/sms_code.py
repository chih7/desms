import re

from desms.constants import VERIFICATION_KEYWORDS_REGEX, LEVEL_NONE, LEVEL_DIGITAL_6, LEVEL_DIGITAL_4, \
    LEVEL_DIGITAL_OTHERS, LEVEL_CHARACTER, LEVEL_TEXT


def contains_chinese(text):
    """是否包含中文"""
    regex = "[\u4e00-\u9fa5]|。"
    return re.search(regex, text)


def contains_keywords(text):
    """是否包含验证码短信关键字"""
    keywords_regex = VERIFICATION_KEYWORDS_REGEX
    return re.search(keywords_regex, text)


# def contains_keywords(keywords_regex, text):
#     """是否包含验证码短信关键字"""
#     return re.search(keywords_regex, text)


def parse_sms_code_if_exists(text):
    """解析文本中的验证码并返回，如果不存在返回空字符"""
    result = parse_by_custom_rules(text)
    if not result:
        result = parse_by_default_rule(text)
    return result


def parse_by_custom_rules(text):
    """Parse SMS code by custom rules"""
    return None


def parse_by_default_rule(text):
    """Parse SMS code by default rule"""
    result = ""
    if contains_keywords(text):
        if contains_chinese(text):
            result = get_sms_code_cn(text)
        else:
            result = get_sms_code_en(text)
    return result


def get_sms_code_cn(text):
    """获取中文短信中包含的验证码"""
    code_regex = "(?<![\d.])[0-9]+(?![\d.])"
    return get_sms_code(code_regex, text)


def get_sms_code_en(text):
    """获取英文短信包含的验证码"""
    code_regex = "(?<![\d.])[0-9]+(?![\d.])"
    return get_sms_code(code_regex, text)


def get_sms_code(code_regex, text):
    """Parse SMS code"""
    possible_codes = []
    codes = re.findall(code_regex, text)
    for code in codes:
        if 4 <= len(code) <= 8 and '.' not in code:
            possible_codes.append(code)
    if not possible_codes:
        return ""

    max_match_level = LEVEL_NONE
    sms_code = ""
    for possible_code in possible_codes:
        if is_near_keywords(possible_code, text):
            cur_level = get_match_level(possible_code)
            if cur_level > max_match_level:
                max_match_level = cur_level
                sms_code = possible_code

    # no possible code near to keywords
    if max_match_level == LEVEL_NONE:
        for possible_code in possible_codes:
            cur_level = get_match_level(possible_code)
            if cur_level > max_match_level:
                max_match_level = cur_level
                sms_code = possible_code

    return sms_code


def get_match_level(text):
    """get match level"""
    if re.search("^[0-9]{6}$", text):
        return LEVEL_DIGITAL_6
    if re.search("^[0-9]{4}$", text):
        return LEVEL_DIGITAL_4
    if re.search("^[0-9]*$", text):
        return LEVEL_DIGITAL_OTHERS
    if re.search("^[a-zA-Z]*$", text):
        return LEVEL_CHARACTER
    return LEVEL_TEXT


def is_near_keywords(matched_str, text):
    """匹配上的字符串是否靠近关键字"""
    begin_index = 0
    end_index = len(text) - 1
    cur_index = text.index(matched_str)
    magic_number = 14
    if cur_index - magic_number > 0:
        begin_index = cur_index = magic_number
    if cur_index + len(matched_str) + magic_number < end_index:
        end_index = cur_index + len(matched_str) + magic_number
    return contains_keywords(text[begin_index:end_index])


if __name__ == "__main__":
    text = "您实名注册的验证码是：100473。为保障信息安全，请勿告诉他人。【中国税务1236600】"
    print(get_sms_code_cn(text))
