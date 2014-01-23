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
    capitalize = False    # upper first letter if True

Retuns translated text.

get_slugify
------------
.. code:: python

    pretranslate = None               # function or dict for replace before translation
    translate = unidecode.unidecode   # function for slugifying or None
    # + slugify's keyword args
    
Returns slugify function.

Examples
==========
.. code-block:: python

    from slugify import slugify, get_slugify, slugify_unicode, slugify_ru

    slugify('one kožušček')                       # one-kozuscek
    slugify('one-=-two-%-three', separator='.')   # one.two.three
    slugify('one two Three', capitalize=True)     # One-two-Three
    slugify('one two three four', max_length=12)  # one-two-four   (12 chars)

    slugify('Я ♥ борщ')                           # Ia-borshch  (standard translation)
    slugify_ru('Я ♥ борщ')                        # Ya-borsch   (alternative russian translation)
    slugify_unicode('Я ♥ борщ')                   # Я-борщ      (sanitize only)

    my_slugify = get_slugify(pretranslate={'я': 'i', '♥': 'love', 'щ': 'sch'}, separator='.')
    my_slugify('Я ♥ борщ')                        # I.love.borsch  (custom translate)

