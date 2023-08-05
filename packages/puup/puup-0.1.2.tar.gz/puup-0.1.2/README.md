# Potentially Universally Unique Phrase generator

## Installation

```
pip install puup
```

## Usage

### Python

```python
>>> import puup
>>> puup.puup()
('crookedly', 'genetically', 'planar', 'tobramycin')
>>> puup.puup('an')
('six', 'filthiness')
>>> puup.puup('van')
('zest', 'insomniac', 'lifestyle')
>>> puup.puup('pan')
('throughout', 'indigent', 'suckerfish')
>>> puup.puup('[if][we]v')
('if', 'we', 'repeat')
>>> puup.puup('[we][can]v[and]v')
('we', 'can', 'carbonate', 'and', 'muddle')
>>> puup.puup('{anprsv}[is][a][very][random][word]')
('beanstalk', 'is', 'a', 'very', 'random', 'word')
```

### Shell

```
$ puup
cosmetically nigh funded antiprotozoal
$ puup --help
Usage: puup [OPTIONS]

  Generate a Potentially Universally Unique Phrase.

Options:
  -t, --template TEMPLATE        [default: rran]
  -P, --prefix TEMPLATE
  -S, --suffix TEMPLATE
  -s, --separator STRING         [default:  ]
  -o, --output FILENAME
  -O, --output-type [text|json]  [default: text]
  -n, --n INTEGER                [default: 1]
  -e, --entropy
  --help                         Show this message and exit.
```
