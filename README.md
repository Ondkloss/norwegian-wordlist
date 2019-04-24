# Norwegian wordlist

Simple project to create a list of Norwegian words. To run:

    python word_parser.py

Example output (and working wordlist) is `wordlist_20190123_norsk_ordbank_nob_2005.txt` and `wordlist_20190123_norsk_ordbank_nno_2012.txt`.

You can also provide `--length` (`-l`) or `--pattern` (`-p`) to filter the wordlist. Some examples:

    python word_parser.py --help
    python word_parser.py --length 4
    python word_parser.py --length 3-5
    python word_parser.py --length 7-*
    python word_parser.py --pattern '.*ubåt.*'
    python word_parser.py -l 7-* -p 'a.+sin'

To handle sorting of ÆØÅ you can include the PyICU module. This also fixes some diacritic issues (EÉÈÊ), but might give some illogical results for AA sorted as Å.

## Source

The bokmål source material is from [Norsk Ordbank in Norwegian Bokmål 2005](https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-5&lang=en), the 2019-02-20 update. It is released under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).

The nynorsk source material is from [Norsk Ordbank in Norwegian Nynorsk 2012](https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-41&lang=en), the 2019-02-20 update. It is released under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).

## Software license

The software in this repo is licensed under WTFPL and can be read in `LICENSE`.

## Known issues

* The regex to remove proper nouns also removes several valid words as well.
* One might evaluate also removing some additional special characters, for example `1`, `2`, `3`, `4` and `/`.
