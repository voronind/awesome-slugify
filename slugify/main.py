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

# Python 3 support
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


def get_sanitize(safe_chars):

    apostrophe_is_not_safe = "'" not in safe_chars

    if '_' in safe_chars:
        unwanted_chars_pattern_template = u'{unwanted_char_pattern}+'
    else:
        unwanted_chars_pattern_template = u'(?:{unwanted_char_pattern}|_)+'
    unwanted_char_pattern = u'[^\w{safe_chars}]'.format(safe_chars=re.escape(safe_chars))
    unwanted_chars_pattern = unwanted_chars_pattern_template.format(unwanted_char_pattern=unwanted_char_pattern)
    unwanted_chars_re = re.compile(unwanted_chars_pattern, re.UNICODE)

    def sanitize(text):
        if apostrophe_is_not_safe:
            text = text.replace("'", '').strip()  # remove '
        return filter(None, unwanted_chars_re.split(text))  # split by unwanted characters

    return sanitize


def join_words(words, separator, max_length=None):

    if not max_length:
        return separator.join(words)

    words = iter(words)   # Python 2 compatible
    text = next(words)    # text = words.pop(0)
    for word in words:
        if len(text + separator + word) <= max_length:
            text += separator + word

    return text[:max_length]


def get_slugify(pretranslate=None, translate=translate, safe_chars='',
                max_length=None, separator=u'-', capitalize=False):

    pretranslate = get_pretranslate(pretranslate)
    sanitize = get_sanitize(safe_chars)

    def slugify(text, max_length=max_length, separator=separator, capitalize=capitalize):
        if not isinstance(text, unicode):
            text = unicode(text, 'utf8', 'ignore')

        if pretranslate:
            text = pretranslate(text)
        if translate:
            text = translate(text)
        words = sanitize(text)
        text = join_words(words, separator, max_length)

        if capitalize:
            text = text[0].upper() + text[1:]

        return text

    return slugify


slugify = get_slugify()
slugify_ru = get_slugify(pretranslate=ALT_CYRILLIC)
slugify_unicode = get_slugify(translate=None)
