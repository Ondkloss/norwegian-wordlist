import re
import tarfile
import os
from argparse import ArgumentParser, ArgumentTypeError

BOKMAL_PATTERN = r'^\d{8}_norsk_ordbank_nob_2005\.tar\.gz$'
NYNORSK_PATTERN = r'^\d{8}_norsk_ordbank_nno_2012\.tar\.gz$'


def find_tar_filename(filename_pattern):
    os.listdir('.')
    results = [f for f in os.listdir('.') if re.search(filename_pattern, f)]

    if len(results) == 1:
        extension_index = results[0].find(".")
        return results[0][:extension_index]

    raise ValueError('Found none or multiple tarballs for pattern {}.'.format(filename_pattern))


def extract_tar(filename):
    tar = tarfile.open(filename, "r:gz")
    tar.extractall()
    tar.close()


def find_lemma_file(directory):
    for file in os.listdir(directory):
        match = re.match(r'^lemma(?:_\d+)?\.txt$', file)
        if match:
            return file


def get_file_contents(filename):
    with open(filename, 'r', encoding='cp1252') as content_file:
        content = content_file.read()

    return content


def set_file_contents(filename, lines):
    with open(filename, "w", encoding='utf8', newline='\n') as text_file:
        text_file.write('\n'.join(lines))


def strip_column_headers(lines):
    return lines[1:]


def filter_pattern(lines, pattern, include):
    result = []

    for line in lines:
        match = re.match(pattern, line)
        if (include and match) or (not include and not match):
            result.append(line)

    return result


def filter_out_pattern(lines, pattern):
    return filter_pattern(lines, pattern, False)


def matching_pattern(lines, pattern):
    if pattern is not None:
        return filter_pattern(lines, pattern, True)

    return lines


def extract_word(lines):
    result = []

    for line in lines:
        match = re.match(r'^\d+\t\d+\t(.+)\t.+$', line)
        if match:
            result.append(match.group(1))

    return result


def remove_proper_nouns(lines):
    # this removed some valid words as well
    return filter_out_pattern(lines, r'^[ÆØÅA-Z].*$')


def remove_word_starts_and_endings(lines):
    return filter_out_pattern(lines, r'^(?:-.*|.*-)$')


def remove_words_with_special_characters(lines):
    # might evaluate removing 1234/ as well
    return filter_out_pattern(lines, r'^.*[\'\$%&°\.\(\) ].*$')


def remove_single_letter_words(lines):
    return filter_out_pattern(lines, r'^.{1}$')


def sort_locale(lines):
    try:
        import PyICU
    except ImportError:
        PyICU = None

    if PyICU:
        collator = PyICU.Collator.createInstance(PyICU.Locale('nb_NO'))
        return sorted(lines, key=collator.getSortKey)
    else:
        print("To get locale specific sorting (æøå) the PyICO module is required. Doing basic sort.")
        return sorted(lines)


def filter_length(lines, minimum, maximum):
    return [line for line in lines if in_interval(line, minimum, maximum)]


def in_interval(item, minimum, maximum):
    item_length = len(item)

    if minimum is not None and item_length < minimum:
        return False
    elif maximum is not None and item_length > maximum:
        return False

    return True


def parse_into_wordlist(filename_pattern, minmax=(None, None), pattern=None):
    # prepare content
    filename = find_tar_filename(filename_pattern)
    extract_tar('{}.tar.gz'.format(filename))
    lemma = find_lemma_file(filename)
    content = get_file_contents('{}/{}'.format(filename, lemma))
    lines = content.split('\n')

    # process lines
    lines = strip_column_headers(lines)
    lines = extract_word(lines)
    lines = set(lines)
    lines = remove_proper_nouns(lines)
    lines = remove_word_starts_and_endings(lines)
    lines = remove_words_with_special_characters(lines)
    lines = remove_words_with_special_characters(lines)
    lines = remove_single_letter_words(lines)
    lines = sort_locale(lines)

    # input filters
    lines = filter_length(lines, *minmax)
    lines = matching_pattern(lines, pattern)

    # persist result
    set_file_contents('wordlist_{}.txt'.format(filename), lines)


# https://stackoverflow.com/a/6512463
def limited_range(value):
    groups = value.split('-')

    if len(groups) < 1 or len(groups) > 2:
        raise ArgumentTypeError("Invalid range format. Expected format similar to '2', '2-4' or '2-*'")

    start = None if groups[0] == '*' else int(groups[0])
    end = (None if groups[1] == '*' else int(groups[1])) if len(groups) > 1 else start

    if start is not None and end is not None and start > end:
        raise ArgumentTypeError("Invalid range. Minimum cannot exceed maximum")

    return (start, end)


def argparser():
    parser = ArgumentParser(description='Create wordlist text file from norsk_ordbank tarballs')
    parser.add_argument('-l', '--length', type=limited_range, help='A length or length range (e.g. "2", "2-4", "2-*" or "*-4")', default=(None, None))
    parser.add_argument('-p', '--pattern', type=str, help='A regex pattern to match (e.g. "a.+sin")', default=None)

    return parser.parse_args()


if __name__ == "__main__":
    args = argparser()
    parse_into_wordlist(BOKMAL_PATTERN, minmax=args.length, pattern=args.pattern)
    parse_into_wordlist(NYNORSK_PATTERN, minmax=args.length, pattern=args.pattern)
