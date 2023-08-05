import functools
import math

import puup.template
import puup.words


@functools.lru_cache
def estimate(template):
    '''estimate template's entropy'''

    e, n = 0, None
    for t, x in puup.template.parse(template):
        if t == 'pos':
            words = puup.words.get(x)
            e += math.log(len(words)) / math.log(2)
            if n is None:
                n = len(words)
            else:
                n *= len(words)

    return (e, n)
