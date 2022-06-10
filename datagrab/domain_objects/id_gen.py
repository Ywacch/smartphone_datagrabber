import hashlib


def generate_id(*args):
    """
    Accept a list of strings and generate a hash to use as an id
    :param args: strings to be used to generate an id
    :return: md5 hash of the passed arguments
    """
    string = ''
    for arg in args:
        string += ' ' + arg
    hash_algorithm = hashlib.md5()
    hash_algorithm.update(string.encode('utf-8'))
    return hash_algorithm.hexdigest()
