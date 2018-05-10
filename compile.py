import json
import re
import sys

with open(sys.argv[1], 'r') as f:
    parsed = json.loads(f.read())

errors = []

EXPECTED_KEYS = [
    'language',
    'version',
    'words',
]

def expected_toplevel_key_validator(content):
    actual_keys = list(content.keys())

    for key in EXPECTED_KEYS:
        if key not in actual_keys:
            errors.append('Expected toplevel key "{}" not found'.format(key))

EXPECTED_LANGUAGES = ['en']

def language_validator(content):
    if 'language' not in content:
        return

    language = content['language']

    if language not in EXPECTED_LANGUAGES:
        errors.append('Unexpected language "{}"'.format(language))

def unexpected_toplevel_key_validator(content):
    actual_keys = list(content.keys())

    for key in actual_keys:
        if key not in EXPECTED_KEYS:
            errors.append('Unexpected toplevel key "{}" found'.format(key))

def version_validator(content):
    if 'version' not in content:
        return

    version = content['version']
    match = re.match(r'\d+\.\d+\.\d+', version)

    if match is None or match.group() != version:
        errors.append('Invalid version "{}"'.format(version))

def word_is_dictionary_validator(word):
    if not isinstance(word, dict):
        errors.append('Expected word to be dict, got {}'.format(word))

EXPECTED_WORD_KEYS = [
    '',
]

def expected_word_key_validator(word):
    actual_keys = list(word.keys())

    for key in EXPECTED_WORD_KEYS:
        if key not in actual_keys:
            errors.append('Expected toplevel key "{}" not found'.format(key))

def unexpected_word_key_validator(word):
    actual_keys = list(word.keys())

    for key in actual_keys:
        if key not in EXPECTED_WORD_KEYS:
            errors.append('Unexpected toplevel key "{}" found'.format(key))

WORD_VALIDATORS = [
    expected_word_key_validator,
    unexpected_word_key_validator,
]

def words_validator(content):
    if 'words' not in content:
        return

    words = content['words']

    if not isinstance(words, list):
        errors.append('Expected "words" to be a list')
        return

    for word in words:
        for validator in WORD_VALIDATORS:
            validator(word)

def words_sorter(content):
    if 'words' not in content:
        return

    content['words'] = sorted(content['words'], key=lambda w: w.get(''))

VALIDATORS = [
    expected_toplevel_key_validator,
    language_validator,
    unexpected_toplevel_key_validator,
    version_validator,
    words_sorter,
]

for validator in VALIDATORS:
    validator(parsed)

if errors:
    for e in errors:
        print(e)
else:
    with open(sys.argv[1] + '.out', 'w') as f:
        f.write(json.dumps(parsed, indent=2, sort_keys=True))
