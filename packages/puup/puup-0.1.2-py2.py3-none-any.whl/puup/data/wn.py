import sys

from nltk.corpus import wordnet as wn


parts_of_speech = {'n': 'noun',
                   'v': 'verb',
                   'a': 'adjective',
                   'r': 'adverb',
                   's': 'adjective satellite'}


def main():
    try:
        pos = sys.argv[1].split('.', 1)[0]
    except IndexError:
        sys.exit(1)

    words = set()
    for ss in wn.all_synsets(pos):
        lemmas = {lem.name() for lem in ss.lemmas()}
        words.update({name for name in lemmas
                      if name.isalpha() and name.islower()})

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
