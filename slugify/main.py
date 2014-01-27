# coding=utf8

import re
import sys
from unidecode import unidecode

ALT_CYRILLIC = {
    u'ё': u'e',    # instead of 'io' / 'yo'
    u'ж': u'j',    # instead of 'zh'
    u'у': u'y',    # instead of 'u'
    u'х': u'h',    # instead of 'kh'
    u'щ': u'sch',  # instead of 'shch'
    u'ю': u'u',    # instead of 'iu' / 'yu'
    u'я': u'ya',   # instead of 'ia'
}

#UNWANTED_CHARS_RE = re.compile(r'[^A-Za-z0-9]+')
UNWANTED_CHARS = re.compile(u'[_\W]+', re.UNICODE)  # all except letters and digits
SEPARATOR = u'-'


if sys.version_info > (3, 0):
    unicode = str


def get_pretranslate(func_dict_none):
    if isinstance(func_dict_none, dict):
        translate_dict = func_dict_none
        # add upper letters
        for letter, translation in list(translate_dict.items()):
            letter_upper = letter.upper()
            if letter_upper != letter and letter_upper not in translate_dict:
                translate_dict[letter_upper] = translation.capitalize()

        PRETRANSLATE = u'({0})'.format('|'.join(map(re.escape, translate_dict)))
        PRETRANSLATE = re.compile(PRETRANSLATE, re.UNICODE)

        def pretranslate(text):
            # translate some letters before translating
            return PRETRANSLATE.sub(lambda m: translate_dict[m.group(1)], text)

        return pretranslate
    else:
        return func_dict_none


def translate(text):
    text = unidecode(text)  # слово -> slovo, returns <type 'str'>
    if not isinstance(text, unicode):
        text = unicode(text, 'utf8', 'ignore')

    #text = unicodedata.normalize('NFKD', text)  # split umlauts and so on
    return text


def sanitize(text):
    text = text.replace("'", '').strip()  # remove '
    words = filter(None, UNWANTED_CHARS.split(text))  # split by unwanted characters
    return words


def join_words(words, max_length=None, separator=SEPARATOR):

    if not max_length:
        return separator.join(words)

    words = iter(words)   # Python 2 compatible
    text = next(words)    # text = words.pop(0)
    for word in words:
        if len(text + separator + word) <= max_length:
            text += separator + word

    return text[:max_length]


def get_slugify(pretranslate=None, translate=translate, max_length=None, separator=SEPARATOR, capitalize=False):

    pretranslate = get_pretranslate(pretranslate)

    def slugify(text, max_length=max_length, separator=separator, capitalize=capitalize):
        if not isinstance(text, unicode):
            text = unicode(text, 'utf8', 'ignore')

        if pretranslate:
            text = pretranslate(text)
        if translate:
            text = translate(text)
        words = sanitize(text)
        text = join_words(words, max_length, separator)

        if capitalize:
            text = text[0].upper() + text[1:]

        return text

    return slugify


slugify = get_slugify()
slugify_ru = get_slugify(pretranslate=ALT_CYRILLIC)
slugify_unicode = get_slugify(translate=None)