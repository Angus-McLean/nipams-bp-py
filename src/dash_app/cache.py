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




import fakeredis
import hashlib
import io
import json
import os
import pandas as pd
import plotly
import redis
import warnings

class redis_store:
    """Save data to Redis using the hashed contents as the key.
    Serialize Pandas DataFrames as memory-efficient Parquet files.

    Otherwise, attempt to serialize the data as JSON, which may have a
    lossy conversion back to its original type. For example, numpy arrays will
    be deserialized as regular Python lists.

    Connect to Redis with the environment variable `REDIS_URL` if available.
    Otherwise, use FakeRedis, which is only suitable for development and
    will not scale across multiple processes.
    """
    if 'REDIS_URL' in os.environ:
        r =  redis.StrictRedis.from_url(os.environ["REDIS_URL"])
    else:
        warnings.warn('Using FakeRedis - Not suitable for Production Use.')
        r = fakeredis.FakeStrictRedis()

    @staticmethod
    def _hash(serialized_obj):
        return hashlib.sha512(serialized_obj).hexdigest()

    @staticmethod
    def save(value):
        if value is None : return
        if isinstance(value, pd.DataFrame):
            buffer = io.BytesIO()
            value.to_parquet(buffer, compression='gzip')
            buffer.seek(0)
            df_as_bytes = buffer.read()
            hash_key = redis_store._hash(df_as_bytes)
            type = 'pd.DataFrame'
            serialized_value = df_as_bytes
        else:
            serialized_value = json.dumps(value, cls=plotly.utils.PlotlyJSONEncoder).encode('utf-8')
            hash_key = redis_store._hash(serialized_value)
            type = 'json-serialized'

        redis_store.r.set(
            f'_dash_aio_components_value_{hash_key}',
            serialized_value
        )
        redis_store.r.set(
            f'_dash_aio_components_type_{hash_key}',
            type
        )
        return hash_key

    @staticmethod
    def load(hash_key):
        if hash_key is None : return
        data_type = redis_store.r.get(f'_dash_aio_components_type_{hash_key}')
        serialized_value = redis_store.r.get(f'_dash_aio_components_value_{hash_key}')
        try:
            if data_type == b'pd.DataFrame':
                value = pd.read_parquet(io.BytesIO(serialized_value))
            else:
                value = json.loads(serialized_value)
        except Exception as e:
            print(e)
            print(f'ERROR LOADING {data_type - hash_key}')
            raise e
        return value