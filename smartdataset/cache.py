import pickle
import shutil
import uuid
from multiprocessing.pool import ThreadPool
from pathlib import Path

from .config import cache_dir, max_cache_count


def make_base_cache_dir():
    make_cache_dir('')


def get_item_uuid(path):
    return uuid.uuid3(uuid.NAMESPACE_URL, str(path)).hex


def make_cache_dir(name):
    path = Path(cache_dir, name)
    if path.exists():
        if not path.is_dir():
            raise OSError(
                f'Cache path {path.absolute()} already exists as a file')
        else:
            return
    path.mkdir()


def cache(file_name, content):
    with open(file_name, 'wb') as file:
        pickle.dump(content, file)


def clear_cache():
    path = Path(cache_dir)
    shutil.rmtree(path)
    make_base_cache_dir()

"""
class CacheThread(threading.Thread):
    def __init__(self, q: queue.Queue, name: str):
        super(CacheThread, self).__init__()
        self._q = q
        self._name = name

    def run(self):
        while self._q.qsize():
            tmp = self._q.get()
            t = tmp[0]

            if t == 'ADD':
                cache(*tmp[1:])
            elif t == 'DEL':
                remove_cache_item(self._name)
            else:
                raise TypeError(f'The CacheThread type {t} is invalid')

            del t, tmp

    def clone(self):
        return CacheThread(self._q, self._name)

    def clone_and_start(self):
        cloned_thread = self.clone()
        cloned_thread.start()
        return cloned_thread
"""

class CacheQueue:
    def __init__(self, name: str, num_threads=16, items=None):
        self._name = get_item_uuid(name)
        self._pool = ThreadPool(processes=num_threads)

        self._count = 0

        make_cache_dir(self._name)

        if items is not None:
            self.initialize_queue(items)

    def initialize_queue(self, items):
        for path, content in items:
            self._pool.apply_async(self._add, args=(path, content))
            self._count += 1
        self._pool.join()

    def add(self, path, content):
        self._pool.apply_async(self._add, args=(path, content))
    
    def _add(self, path, content):
        cache(path, content)

        self._count += 1

        if self._count > max_cache_count:
            self.remove()

    def remove(self):
        self._pool.apply_async(self._remove)
    
    def _remove(self):
        files = list(Path(cache_dir, self._name).glob('*'))
        files.sort(key=lambda path: path.stat().st_mtime)
        while True:
            try:
                files[0].unlink()
                break
            except PermissionError:
                pass
        self._count -= 1

    def cache_wrapper(self, func):
        def wrapper(item):
            cache_path = get_item_uuid(item)
            path = Path(cache_dir, self._name, cache_path)

            if path.exists():
                with open(path, 'rb') as file:
                    return pickle.load(file)
            else:
                r = func(item)

                self.add(path, r)
                return r

        return wrapper
