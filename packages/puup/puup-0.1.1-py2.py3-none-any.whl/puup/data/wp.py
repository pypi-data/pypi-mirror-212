import re
import sys

import httpx


parts_of_speech = {'p': 'preposition'}


def main():
    try:
        pos = sys.argv[1].split('.', 1)[0]
    except IndexError:
        sys.exit(1)

    page = {'p': 'List_of_English_prepositions'}.get(pos)
    words = set()

    with httpx.Client(base_url='https://en.wikipedia.org/w/') as client:
        data = client.get('api.php', params={
            'action': 'parse',
            'page': page,
            'prop': 'iwlinks',
            'format': 'json',
        }).json()
        for link in data['parse']['iwlinks']:
            text = link['*']
            m = re.match(r'wikt:([a-z]+)$', text)
            if m:
                words.add(m.group(1))

    words = list(words)
    words.sort()

    print('# ' + parts_of_speech[pos] + 's')
    print('words = (')
    for i, word in enumerate(words):
        if i > 0:
            print(',')
        print("  '" + word + "'", end='')
    print('\n)')


if __name__ == '__main__':
    main()
