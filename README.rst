====================
awesome-slugify
====================

**Python flexible slugify function**

| PyPi: https://pypi.python.org/pypi/awesome-slugify
| Github: https://github.com/dimka665/awesome-slugify


Install
==========
.. code-block:: bash

    pip install awesome-slugify

Usage
======

.. code-block:: python

    from slugify import slugify
    
    slugify('Any text')  # 'Any-text'
    
Custom slugify
================

.. code-block:: python

    from slugify import slugify, Slugify

    slugify('Any text', to_lower=True)  # 'any-text'

    custom_slugify = Slugify(to_lower=True)
    custom_slugify('Any text')          # 'any-text'

    custom_slugify.separator = '_'
    custom_slugify('Any text')          # 'any_text'

slugify function optional args
--------------------------------

.. code-block:: python

    to_lower              # if True convert text to lowercase
    max_length            # output string max length
    separator             # separator string
    capitalize            # if True upper first letter


Slugify class args
---------------------

.. code-block:: python

    pretranslate = None               # function or dict for replace before translation
    translate = unidecode.unidecode   # function for slugifying or None
    safe_chars = ''                   # additional safe chars
    stop_words = ()                   # remove these words from slug

    to_lower = False                  # default to_lower value
    max_length = None                 # default max_length value
    separator = '-'                   # default separator value
    capitalize = False                # default capitalize value

Predefined slugify functions
==============================

Some slugify functions is predefined this way:

.. code-block:: python

    from slugify import Slugify, CYRILLIC, GERMAN, GREEK

    slugify = Slugify()
    slugify_unicode = Slugify(translate=None)

    slugify_url = Slugify()
    slugify_url.to_lower = True
    slugify_url.stop_words = ('a', 'an', 'the')
    slugify_url.max_length = 200

    slugify_filename = Slugify()
    slugify_filename.separator = '_'
    slugify_filename.safe_chars = '-.'
    slugify_filename.max_length = 255

    slugify_ru = Slugify(pretranslate=CYRILLIC)
    slugify_de = Slugify(pretranslate=GERMAN)
    slugify_el = Slugify(pretranslate=GREEK)

Examples
==========

.. code-block:: python

    from slugify import Slugify, slugify, slugify_unicode
    from slugify import slugify_url, slugify_filename
    from slugify import slugify_ru, slugify_de
    
    slugify('one kožušček')                       # one-kozuscek
    slugify('one two three', separator='.')       # one.two.three
    slugify('one two three four', max_length=12)  # one-two-four   (12 chars)
    slugify('one TWO', to_lower=True)             # one-two
    slugify('one TWO', capitalize=True)           # One-TWO
    
    slugify_filename(u'Дrаft №2.txt')             # Draft_2.txt
    slugify_url(u'Дrаft №2.txt')                  # draft-2-txt
    
    my_slugify = Slugify()
    my_slugify.separator = '.'
    my_slugify.pretranslate = {'я': 'i', '♥': 'love'}
    my_slugify('Я ♥ борщ')                        # I.love.borshch  (custom translate)
    
    slugify('Я ♥ борщ')                           # Ia-borshch  (standard translation)
    slugify_ru('Я ♥ борщ')                        # Ya-borsch   (alternative russian translation)
    slugify_unicode('Я ♥ борщ')                   # Я-борщ      (sanitize only)

    slugify_de('ÜBER Über slugify')               # UEBER-Ueber-slugify

