# coding: utf-8
from unittest import TestCase
from name_conversion.enums import Case, Gender
from name_conversion.converter import Converter

__author__ = 'damirazo <me@damirazo.ru>'


class ConverterTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.p = Converter()

    def test_1(self):
        self.assertEqual(self.p.firstname(u'Дамир', Case.GENITIVE), u'Дамира')

    def test_2(self):
        self.assertEqual(self.p.lastname(u'Абдуллин', Case.PREPOSITIONAL), u'Абдуллине')

    def test_3(self):
        self.assertEqual(self.p.lastname(u'Каримова', Case.DATIVE), u'Каримовой')

    def test_4(self):
        self.assertEqual(self.p.middlename(u'Васильевич', Case.DATIVE), u'Васильевичу')

    def test_5(self):
        self.assertEqual(self.p.lastname(u'Ткач', Case.GENITIVE, gender=Gender.FEMALE), u'Ткач')

    def test_6(self):
        self.assertEqual(self.p.lastname(u'Ткач', Case.GENITIVE, gender=Gender.MALE), u'Ткача')
