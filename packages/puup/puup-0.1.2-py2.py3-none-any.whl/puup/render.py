import secrets

import puup.template
import puup.words


def render(template):
    for t, x in puup.template.parse(template):
        if t == 'pos':
            try:
                yield secrets.choice(puup.words.get(x))
            except ValueError as e:
                raise ValueError((template,) + e.args)
        elif t == 'literal':
            yield x
