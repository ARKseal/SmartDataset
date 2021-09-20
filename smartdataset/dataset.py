from .cache import CacheQueue
from .pytorch import IterableDataset
from .utils import new_name


def base_preprocess_f(item):
    return item


class SmartDataset(IterableDataset):
    def __init__(self, items,  name=None, preprocess_f=None):
        if preprocess_f is None:
            preprocess_f = base_preprocess_f

        if name is None:
            name = new_name()
        print(f'SmartDataset init: name={name}')

        assert callable(preprocess_f)

        self._name = name
        self._items = items
        self._cache_queue = CacheQueue(name)
        self._preprocess_f = self._cache_queue.cache_wrapper(
            preprocess_f)

    def __iter__(self):
        for item in self._items:
            yield self._preprocess_f(item)
