# coding: utf8

import unittest
from slugify import slugify, slugify_unicode, slugify_ru, get_slugify


class SlugifyTestCase(unittest.TestCase):

    def test_slugify_english(self):
        self.assertEqual(slugify('This % is a test ---'), 'This-is-a-test')
        self.assertEqual(slugify('_this_is_a__test___'), 'this-is-a-test')
        self.assertEqual(slugify('- - -This -- is a ## test ---'), 'This-is-a-test')

    def test_slugify_umlaut(self):
        self.assertEqual(slugify('kožušček'), 'kozuscek',)
        self.assertEqual(slugify('C\'est déjà l\'été.'), 'Cest-deja-lete')
        self.assertEqual(slugify('jaja---lol-méméméoo--a'), 'jaja-lol-mememeoo-a')
        self.assertEqual(slugify('Nín hǎo. Wǒ shì zhōng guó rén'), 'Nin-hao-Wo-shi-zhong-guo-ren')
        self.assertEqual(slugify('Programmes de publicité - Solutions d\'entreprise'), 'Programmes-de-publicite-Solutions-dentreprise')

    def test_slugify_chinese(self):
        self.assertEqual(slugify('北亰'), 'Bei-Jing')

    def test_slugify_russian(self):
        self.assertEqual(slugify('Компьютер'), 'Kompiuter')
        self.assertEqual(slugify('Транслитерирует и русский'), 'Transliteriruet-i-russkii')
        self.assertEqual(slugify('ёжик из щуки сварил уху'), 'iozhik-iz-shchuki-svaril-ukhu')
        self.assertEqual(slugify('Ах, Юля-Юля'), 'Akh-Iulia-Iulia')

    def test_slugify_russian_alt(self):
        self.assertEqual(slugify_ru('Компьютер'), 'Komputer')
        self.assertEqual(slugify_ru('Транслитерирует и русский'), 'Transliteriryet-i-rysskii')
        self.assertEqual(slugify_ru('ёжик из щуки сварил уху'), 'ejik-iz-schyki-svaril-yhy')
        self.assertEqual(slugify_ru('Ах, Юля-Юля'), 'Ah-Ulya-Ulya')

    def test_slugify_unicode(self):
        self.assertEqual(slugify_unicode('-=Слово по-русски=-'), u'Слово-по-русски')
        self.assertEqual(slugify_unicode('слово_по_русски'), u'слово-по-русски')


class TruncateTestCase(unittest.TestCase):

    def test_truncate(self):
        self.assertEqual(slugify('one two three four', max_length=7), 'one-two')
        self.assertEqual(slugify('one two three four', max_length=8), 'one-two')
        self.assertEqual(slugify('one two three four', max_length=12), 'one-two-four')
        self.assertEqual(slugify('one two three four', max_length=13), 'one-two-three')
        self.assertEqual(slugify('one two three four', max_length=14), 'one-two-three')

    def test_truncate_short(self):
        self.assertEqual(slugify('dlinnoeslovo', max_length=7), 'dlinnoe')
        self.assertEqual(slugify('dlinnoeslovo и ещё слово', max_length=11), 'dlinnoeslov')

    def test_truncate_long(self):
        self.assertEqual(slugify('шшш щщщ слово', max_length=11), 'shshsh')
        self.assertEqual(slugify('шшш щщщ слово', max_length=12), 'shshsh-slovo')
        self.assertEqual(slugify('шшш щщщ слово', max_length=18), 'shshsh-slovo')
        self.assertEqual(slugify('шшш щщщ слово', max_length=19), 'shshsh-shchshchshch')
        self.assertEqual(slugify('шшш щщщ слово', max_length=24), 'shshsh-shchshchshch')
        self.assertEqual(slugify('шшш щщщ слово', max_length=25), 'shshsh-shchshchshch-slovo')

    def test_truncate_unwanted(self):
        self.assertEqual(slugify('...one...two...three...four...', max_length=12), 'one-two-four')

    def test_truncate_long_separator(self):
        self.assertEqual(slugify('one two three four', max_length=14, separator='...'), 'one...two')


class PretranslateTestCase(unittest.TestCase):

    def test_pretranslate(self):
        ALT_TRANSLATION= {
            u'ʘ‿ʘ': u'smiling',
            u'ಠ_ಠ': u'disapproval',
            u'♥‿♥': u'enamored',
            u'♥': u'love',

            u'(c)': u'copyright',
            u'©': u'copyright',
        }
        slugify_emoji = get_slugify(pretranslate=ALT_TRANSLATION)
        self.assertEqual(slugify_emoji(u'ʘ‿ʘ'), u'smiling')
        self.assertEqual(slugify_emoji(u'ಠ_ಠ'), u'disapproval')
        self.assertEqual(slugify_emoji(u'(c)'), u'copyright')
        self.assertEqual(slugify_emoji(u'©'), u'copyright')


class OtherTestCase(unittest.TestCase):

    def test_capitalize(self):
        self.assertEqual(slugify('this Is A test', capitalize=True), 'This-Is-A-test')

    def test_safe_chars(self):
        filename_slugify = get_slugify(safe_chars='-_.', separator='_')
        self.assertEqual(filename_slugify(u'Дrаft №2.txt'), u'Draft_2.txt')


if __name__ == '__main__':
    unittest.main()



