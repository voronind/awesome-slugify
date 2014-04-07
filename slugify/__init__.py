from slugify.main import Slugify
from slugify.alt_translates import *


slugify = Slugify()
slugify_unicode = Slugify(translate=None)

slugify_ru = Slugify(pretranslate=CYRILLIC)
slugify_de = Slugify(pretranslate=GERMAN)
slugify_el = Slugify(pretranslate=GREEK)


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
