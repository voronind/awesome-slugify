====================
awesome-slugify
====================

**Python flexible slugify function**

| PyPi: https://pypi.python.org/pypi/awesome-slugify
| Github: https://github.com/dimka665/awesome-slugify


Install
==========
.. code:: bash

    pip install awesome-slugify
    
Usage
=================

.. code:: python

    from slugify import slugify
    
    slugify(u'Any text')  # u'Any-text'
    
slugify optional args
---------------
.. code:: python

    to_lower              # if True convert text to lowercase
    max_length            # output string max length
    separator             # separator string
    capitalize            # if True upper first letter
    
Custom slugify
================
.. code:: python

    from slugify import Slugify
    
    custom_slugify = Slugify(separator='.')
    custom_slugify(u'Any text')  # u'Any.text'

Slugify args
----------------

.. code-block:: python

    pretranslate = None               # function or dict for replace before translation
    translate = unidecode.unidecode   # function for slugifying or None
    safe_chars = ''                   # additional safe chars
    
    to_lower = False                  # default to_lower value
    max_length = None                 # default max_length value
    separator = '-'                   # default separator value
    capitalize = False                # default capitalize value


Examples
==========
.. code-block:: python

    from slugify import slugify, slugify_unicode, slugify_ru
    from slugify import Slugify
    
    
    slugify('one kožušček')                       # one-kozuscek
    slugify('one two three', separator='.')       # one.two.three
    slugify('one two three four', max_length=12)  # one-two-four   (12 chars)
    slugify('one TWO', capitalize=True)           # One-TWO

    slugify('Я ♥ борщ')                           # Ia-borshch  (standard translation)
    slugify_ru('Я ♥ борщ')                        # Ya-borsch   (alternative russian translation)
    slugify_unicode('Я ♥ борщ')                   # Я-борщ      (sanitize only)
    
    filename_slugify = Slugify(safe_chars='-_.', separator='_')
    filename_slugify(u'Дrаft №2.txt')             # Draft_2.txt

    my_slugify = Slugify(pretranslate={'я': 'i', '♥': 'love', 'щ': 'sch'}, separator='.')
    my_slugify('Я ♥ борщ')                        # I.love.borsch  (custom translate)

