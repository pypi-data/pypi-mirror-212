# -*- coding:utf-8 -*-
# Author:  zhousf
# Date:    2023-02-23
# Description:

def is_number(string: str):
    """
    是否数值，包含int、float、double
    :param string:
    :return:
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_equal_number(string1: str, string2: str):
    """
    数值是否相等
    :param string1: "12"
    :param string2: "12.0"
    :return:
    """
    if is_number(string1) and is_number(string2):
        if float(string1) == float(string2):
            return True
    if string1 == string2:
        return True
    return False


def contains(string: str, what: list):
    for s in what:
        if string.find(s) > -1:
            return True
    return False
