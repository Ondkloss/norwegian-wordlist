import re
import tarfile
import os

BOKMAL = '20180627_norsk_ordbank_nob_2005'
NYNORSK = '20180626_norsk_ordbank_nno_2012'


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
    with open(filename, 'r', encoding='utf8') as content_file:
        content = content_file.read()

    return content


def set_file_contents(filename, lines):
    with open(filename, "w", encoding='utf8', newline='\n') as text_file:
        text_file.write('\n'.join(lines))


def strip_column_headers(lines):
    return lines[1:]


def filter_out_pattern(lines, pattern):
    result = []

    for line in lines:
        match = re.match(pattern, line)
        if not match:
            result.append(line)

    return result


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
    return filter_out_pattern(lines, r'^.*[\'\$%&\.\(\) ].*$')


def remove_single_letter_words(lines):
    return filter_out_pattern(lines, r'^.{1}$')


def parse_into_wordlist(filename):
    # prepare content
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
    lines = sorted(lines)

    # persist result
    set_file_contents('wordlist_{}.txt'.format(filename), lines)


parse_into_wordlist(BOKMAL)
parse_into_wordlist(NYNORSK)
