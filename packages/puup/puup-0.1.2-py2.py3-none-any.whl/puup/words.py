import functools

from puup.lazy import import_module as lazy_import


modules = {pos: lazy_import('.'+pos, 'puup.data') for pos in 'anprsv'}


@functools.lru_cache
def get(pos):
    words = set()
    try:
        if isinstance(pos, tuple):
            words.update(*(modules[p].words for p in pos))
        else:
            words.update(modules[pos].words)
    except KeyError:
        raise ValueError(pos)
    return list(words)
