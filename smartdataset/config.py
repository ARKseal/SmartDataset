import os

from .utils import safe

DEFAULT_CACHE_DIR = './.smartdataset_cache'
DEFAULT_MAX_CACHE_COUNT = '1e15'

cache_dir = os.path.expanduser(os.environ.get(
    'SMARTDATASET_CACHE_DIR', DEFAULT_CACHE_DIR))
max_cache_count = int(
    float(safe(os.environ.get('SMARTDATASET_MAX_CACHE_COUNT', DEFAULT_MAX_CACHE_COUNT))))
