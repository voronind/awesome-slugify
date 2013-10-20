====================
awesome-slugify
====================

**Python slugify module**

| Pypi: https://pypi.python.org/pypi/awesome-slugify
| Github: https://github.com/dimka665/awesome-slugify


Install
==========
.. code:: bash

    pip install awesome-slugify

Use
==========
.. code-block:: python

    from slugify import slugify, get_slugify, slugify_unicode, slugify_ru

    slugify('one kožušček')                       # one-kozuscek
    slugify('one-=-two-%-three', separator='.')   # one.two.three
    slugify('one two three four', max_length=12)  # one-two-four

    slugify('я ♥ борщ')                           # ia-borshch
    slugify_unicode('я ♥ борщ')                   # я-борщ    (sanitize only)

    my_slugify = get_slugify(pretranslate={'я': 'i', '♥': 'love', 'щ': 'sch'}, separator='.')
    my_slugify('я ♥ щи')                          # i.love.borsch  (custom translate)
    
    slugify_ru('я ♥ щи')                          # ya-borsch
    
