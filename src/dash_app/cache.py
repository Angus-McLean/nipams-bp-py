### Cache Functions
CACHE = {}
def set(obj, key=None):
    global CACHE
    try:
        hash_key = hash(obj)
    except:
        hash_key = len(obj)
    key = key or hash_key
    CACHE[key] = obj
    return key

def get(hash_key):
    global CACHE
    return CACHE.get(hash_key)

def has(hash_key):
    global CACHE
    return hash_key in CACHE
