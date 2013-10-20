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

    slugify('я ♥ борщ')                           # ia-borshch
    slugify_unicode('я ♥ борщ')                   # я-борщ    (sanitize only)

    my_slugify = get_slugify(pretranslate={'я': 'i', '♥': 'love', 'щ': 'sch'}, separator='.')
    my_slugify('я ♥ щи')                          # i.love.borsch  (custom translate)
    
    slugify_ru('я ♥ щи')                          # ya-borsch  (alternative russian translate)
    
