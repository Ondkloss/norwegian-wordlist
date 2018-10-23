# Norwegian wordlist

Simple project to create a list of Norwegian words. To run:

    python word_parser.py

An example output (and working wordlist) is `wordlist.txt`.

## Source

The source material is from [Norsk Ordbank in Norwegian Bokmål 2005](https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-5&lang=en), the 2018-06-27 update. It is released under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).

## Known issues

* The regex to remove proper nouns also removes several valid words as well.
* One might evaluate also removing some additional special characters, for example `1`, `2`, `3`, `4` and `/`.
* Å is sorted before Ø.
