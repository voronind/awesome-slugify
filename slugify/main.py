# coding=utf8

import re
import sys
import regex
from unidecode import unidecode

# turn on PCRE version of regex module, incompatible with standard re module
regex.DEFAULT_VERSION = regex.V1


if sys.version_info[0] == 2:
    TEXT_TYPE = unicode  # Python 2
else:
    TEXT_TYPE = str  # Python 3


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

# uppercase letters to translate to uppercase letters, NOT camelcase
UPPER_TO_UPPER_LETTERS_RE = \
    '''
    (
            \p{Uppercase_Letter} {2,}                          # 2 or more adjacent letters - UP always
        |
            \p{Uppercase_Letter}                               # target one uppercase letter, then
                (?=
                    [^\p{Lowercase_Letter}…\p{Term}--,،﹐，]+    # not chars breaks possible UP (…abc.?!:;)
                    \p{Uppercase_Letter} {2}                   # and 2 uppercase letters
                )
        |
            (?<=
                \p{Uppercase_Letter} {2}                       # 2 uppercase letters
                [^\p{Lowercase_Letter}…\p{Term}--,،﹐，]+       # not chars breaks possible UP (…abc.?!:;), then
            )
            \p{Uppercase_Letter}                               # target one uppercase letter, then
            (?!
                    \p{Lowercase_Letter}                       # not lowercase letter
                |
                    […\p{Term}--,،﹐，]\p{Uppercase_Letter}      # and not dot (.?…!:;) with uppercase letter
            )
    )
    '''


class Slugify(object):

    upper_to_upper_letters_re = regex.compile(UPPER_TO_UPPER_LETTERS_RE, regex.UNICODE | regex.VERBOSE)

    def __init__(self, pretranslate=None, translate=unidecode, safe_chars='',
            to_lower=False, max_length=None, separator=u'-', capitalize=False):

        self.to_lower = to_lower
        self.max_length = max_length
        self.separator = separator
        self.capitalize = capitalize

        self.pretranslate = pretranslate
        self.translate = translate
        self.safe_chars = safe_chars

    def pretranslate_dict_to_function(self, convert_dict):

        # add uppercase letters
        for letter, translation in list(convert_dict.items()):
            letter_upper = letter.upper()
            if letter_upper != letter and letter_upper not in convert_dict:
                convert_dict[letter_upper] = translation.capitalize()

        self.convert_dict = convert_dict

        PRETRANSLATE = u'({0})'.format('|'.join(map(re.escape, convert_dict)))
        PRETRANSLATE = re.compile(PRETRANSLATE, re.UNICODE)

        # translate some letters before translating
        return lambda text: PRETRANSLATE.sub(lambda m: convert_dict[m.group(1)], text)

    def set_pretranslate(self, pretranslate):
        if isinstance(pretranslate, dict):
            pretranslate = self.pretranslate_dict_to_function(pretranslate)

        elif pretranslate is None:
            pretranslate = lambda text: text

        elif not callable(pretranslate):
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
        unwanted_chars_re = u'[^\p{{AlNum}}{safe_chars}]+'.format(safe_chars=regex.escape(safe_chars))
        self.unwanted_chars_re = regex.compile(unwanted_chars_re, regex.UNICODE)
        self.apostrophe_is_not_safe = "'" not in safe_chars

    safe_chars = property(fset=set_safe_chars)

    def sanitize(self, text):
        if self.apostrophe_is_not_safe:
            text = text.replace("'", '').strip()  # remove '
        return filter(None, self.unwanted_chars_re.split(text))  # split by unwanted characters

    def __call__(self, text, **kwargs):

        max_length = kwargs.get('max_length', self.max_length)
        separator = kwargs.get('separator', self.separator)

        if not isinstance(text, TEXT_TYPE):
            text = text.decode('utf8', 'ignore')

        if kwargs.get('to_lower', self.to_lower):
            text = text.lower()
            text = self._pretranslate(text)
            text = self._translate(text)

        else:
            text_parts = self.upper_to_upper_letters_re.split(text)

            for position, text_part in enumerate(text_parts):
                text_part = self._pretranslate(text_part)
                text_part = self._translate(text_part)
                if position % 2:
                    text_part = text_part.upper()

                text_parts[position] = text_part

            text = u''.join(text_parts)

        words = self.sanitize(text)
        text = join_words(words, separator, max_length)

        if text and kwargs.get('capitalize', self.capitalize):
            text = text[0].upper() + text[1:]

        return text

# \p{SB=AT} = '.․﹒．'
# \p{SB=ST} = '!?՜՞։؟۔܀܁܂߹।॥၊။።፧፨᙮᜵᜶‼‽⁇⁈⁉⸮。꓿꘎꘏꤯﹖﹗！？｡'
# \p{Term}  = '!,.:;?;·։׃،؛؟۔܀܁܂܃܄܅܆܇܈܉܊܌߸߹।॥๚๛༈།༎༏༐༑༒၊။፡።፣፤፥፦፧፨᙭᙮᛫᛬᛭។៕៖៚‼‽⁇⁈⁉⸮、。꓾꓿꘍꘎꘏꤯﹐﹑﹒﹔﹕﹖﹗！，．：；？｡､'
# \p{Sterm} = '! .  ?՜՞։؟܀   ܁     ܂߹।॥၊။               ።፧፨  ᙮᜵᜶        ‼‽⁇⁈⁉⸮ 。 ꓿ ꘎꘏꤯﹒     ﹖﹗！．    ？｡'

# \p{SB=AT} = .
# \p{SB=ST} =   ! ?
# \p{Term}  = . ! ? , : ;
# \p{Sterm} = . ! ?

# \u002c - Latin comma
# \u060c - Arabic comma
# \ufe50 - Small comma
# \uff0c - Fullwidth comma

# […\p{Term}--,،﹐，] - ellipsis + Terms - commas
