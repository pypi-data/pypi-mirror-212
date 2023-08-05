import functools


@functools.lru_cache
def parse(template):
    def generate():
        group, literal = None, None
        for c in template:
            if group is not None:
                if c == '}':
                    yield ('pos', tuple(group))
                    group = None
                else:
                    group.add(c)
            elif literal is not None:
                if c == ']':
                    yield ('literal', literal)
                    literal = None
                else:
                    literal += c
            else:
                if c == '{':
                    group = set()
                elif c == '[':
                    literal = ''
                else:
                    yield ('pos', c)
    return tuple(generate())
