import hashlib


def calculate_sha256_hash(data):
    sha256_hash = hashlib.sha256()
    if isinstance(data, str):
        data = data.encode('utf-8')
    sha256_hash.update(data)
    hash_result = sha256_hash.hexdigest()
    return hash_result


def mal_ratio(dict_result):
    a = dict_result['malicious'] + dict_result['undetected']
    b = dict_result['malicious']
    return "{}/{}".format(b, a)
