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


def join_words(words, separator, max_length=None):

    if not max_length:
        return separator.join(words)

    words = iter(words)   # List to Generator
    try:
        text = next(words)
    except StopIteration:
        return u''

    for word in words:
        if len(text + separator + word) <= max_length:
            text += separator + word

    return text[:max_length]


class Slugify(object):

    def __init__(self, pretranslate=None, translate=unidecode, safe_chars='',
            max_length=None, separator=u'-', capitalize=False):

        self.max_length = max_length
        self.separator = separator
        self.capitalize = capitalize

        self.pretranslate = pretranslate
        self.translate = translate
        self.safe_chars = safe_chars

    def set_pretranslate(self, pretranslate):
        if isinstance(pretranslate, dict):
            pretranslate_dict = pretranslate
            # add upper letters
            for letter, translation in list(pretranslate_dict.items()):
                letter_upper = letter.upper()
                if letter_upper != letter and letter_upper not in pretranslate_dict:
                    pretranslate_dict[letter_upper] = translation.capitalize()

            PRETRANSLATE = u'({0})'.format('|'.join(map(re.escape, pretranslate_dict)))
            PRETRANSLATE = re.compile(PRETRANSLATE, re.UNICODE)

            # translate some letters before translating
            pretranslate = lambda text: PRETRANSLATE.sub(lambda m: pretranslate_dict[m.group(1)], text)

        elif pretranslate is None:
            pretranslate = lambda text: text

        else:
            error_message = u"Keyword argument 'pretranslate' must be dict, None or callable. Not {0.__class__.__name__}".format(pretranslate)
            raise ValueError(error_message)

        self._pretranslate = pretranslate

    pretranslate = property(fset=set_pretranslate)

    def set_translate(self, func):
        if func:
            self._translate = func
        else:
            self._translate = lambda text: text

    translate = property(fset=set_translate)

    def set_safe_chars(self, safe_chars):
        self.apostrophe_is_not_safe = "'" not in safe_chars

        if '_' in safe_chars:
            unwanted_chars_pattern_template = u'{unwanted_char_pattern}+'
        else:
            unwanted_chars_pattern_template = u'(?:{unwanted_char_pattern}|_)+'

        unwanted_char_pattern = u'[^\w{safe_chars}]'.format(safe_chars=re.escape(safe_chars))
        unwanted_chars_pattern = unwanted_chars_pattern_template.format(unwanted_char_pattern=unwanted_char_pattern)
        self.unwanted_chars_re = re.compile(unwanted_chars_pattern, re.UNICODE)

    safe_chars = property(fset=set_safe_chars)

    def sanitize(self, text):
        if self.apostrophe_is_not_safe:
            text = text.replace("'", '').strip()  # remove '
        return filter(None, self.unwanted_chars_re.split(text))  # split by unwanted characters

    def __call__(self, text, **kwargs):

        max_length = kwargs.get('max_length', self.max_length)
        separator = kwargs.get('separator', self.separator)

        if not isinstance(text, unicode):
            text = unicode(text, 'utf8', 'ignore')

        text = self._pretranslate(text)
        text = self._translate(text)

        if not isinstance(text, unicode):
            text = unicode(text, 'utf8', 'ignore')

        words = self.sanitize(text)
        text = join_words(words, separator, max_length)

        if kwargs.get('capitalize', self.capitalize) and text:
            text = text[0].upper() + text[1:]

        return text


slugify = Slugify()
slugify_ru = Slugify(pretranslate=ALT_CYRILLIC)
slugify_unicode = Slugify(translate=None)

# Legacy code
def deprecate_init(Klass):
    class NewKlass(Klass):
        def __init__(self, *args, **kwargs):
            import warnings
            warnings.simplefilter('once')
            warnings.warn("'slugify.get_slugify' is deprecated; use 'slugify.Slugify' instead.",
                          DeprecationWarning, stacklevel=2)
            super(NewKlass, self).__init__(*args, **kwargs)
    return NewKlass

# get_slugify was deprecated in 2014, march 31
get_slugify = deprecate_init(Slugify)
