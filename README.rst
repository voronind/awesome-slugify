====================
awesome-slugify
====================

**Python slugify package**

Pypi: https://pypi.python.org/pypi/awesome-slugify
Github: https://github.com/dimka665/awesome-slugify


Install
==========
    pip install awesome-slugify

Use
==========
    from slugify import slugify, slugify-unicode,

    slugify('one kožušček')    # u'one-kozuscek'
    slugify('one-=-two-%-three', separator='.')   # one.two.three
    slugify('one two three four', max_length=12)  # one-two-four

    slugify('я ♥ щи')                             # ia-shchi
    
    from slugify import slugify_unicode
    slugify_unicode('я ♥ щи')                     # я-щи    (sanitize only)

    from slugify import get_slugify
    my_slugify = get_slugify(pretranslate={'я': 'i', '♥': 'love', 'щ': 'sch'}, separator='.')
    my_slugify('я ♥ щи')                         # i.love.schi  (custom translate)
    

    


    
