import uuid


def get_id(l=8):
    u = ''
    uhex = uuid.uuid4().hex
    encoded = ''.join(filter(str.isalnum, uhex))
    u = encoded[:l].upper()
    return u