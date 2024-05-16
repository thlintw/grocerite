import uuid, os


def get_id(l=8):
    u = ''
    uhex = uuid.uuid4().hex
    encoded = ''.join(filter(str.isalnum, uhex))
    u = encoded[:l].upper()
    return u


def get_collection_name_suffix(name):
    test_suffix = ''
    if os.getenv('APP_MODE') == 'dev':
        test_suffix = '_test'

    return f'{name}{test_suffix}'