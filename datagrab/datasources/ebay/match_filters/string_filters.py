import re


def remove_unicode(string):
    """
    Convert all unicodes into whitespace
    :param string: string containing unicode strings
    :return: string withh all ascii characters
    """
    unicodeless = string.encode('ascii', 'replace').decode()
    return unicodeless.replace("?", " ")


def split_words(string):
    """
    Split a sting into words according to typographical symbols and punctuation marks
    :param string: String wo be split
    :return: List of split strings
    """
    try:
        strings = re.split(r",|_|-|!|\\| |\(|\)|\/|\[|\]|\||'", string)
    except:  # tbh forgot why this is here just got it from my previous code
        strings = re.split(", |_|-|!|'", string)

    # remove empty strings
    string_list = [string for string in strings if string]
    return string_list
