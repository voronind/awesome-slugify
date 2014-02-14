====================
awesome-slugify
====================

**Python flexible slugify module**

| Pypi: https://pypi.python.org/pypi/awesome-slugify
| Github: https://github.com/dimka665/awesome-slugify


Install
==========
.. code:: bash

    pip install awesome-slugify
    
Function args
=================

slugify
---------
.. code:: python

    text                  # text for translate. position arg
    max_length = None     # output string max length
    separator = '-'       # separator string
    capitalize = False    # if True upper first letter

Retuns translated text.

get_slugify
------------
.. code:: python

    pretranslate = None               # function or dict for replace before translation
    translate = unidecode.unidecode   # function for slugifying or None
    safe_chars = ''                   # additional safe chars
    # + slugify's keyword args
    
Returns slugify function.

Examples
==========
.. code-block:: python

    from slugify import slugify, slugify_unicode, slugify_ru
    from slugify import get_slugify
    
    
    slugify('one kožušček')                       # one-kozuscek
    slugify('one two three', separator='.')       # one.two.three
    slugify('one two three four', max_length=12)  # one-two-four   (12 chars)
    slugify('one TWO', capitalize=True)           # One-TWO

    slugify('Я ♥ борщ')                           # Ia-borshch  (standard translation)
    slugify_ru('Я ♥ борщ')                        # Ya-borsch   (alternative russian translation)
    slugify_unicode('Я ♥ борщ')                   # Я-борщ      (sanitize only)
    
    filename_slugify = get_slugify(safe_chars='-_.', separator='_')
    filename_slugify(u'Дrаft №2.txt')             # Draft_2.txt

    my_slugify = get_slugify(pretranslate={'я': 'i', '♥': 'love', 'щ': 'sch'}, separator='.')
    my_slugify('Я ♥ борщ')                        # I.love.borsch  (custom translate)

