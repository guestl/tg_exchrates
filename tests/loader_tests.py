# run me as "nosetests -v --with-coverage --cover-inclusive --cover-package="tg_exchrates""
from nose.tools import *

#from tg_exchrates import loader_kz_nb

import os
#import sys
#import io
import codecs
import datetime

from loader_kz_nb import Loader_KZ_NB
from loader_kz_kkb_exchp import Loader_KZ_KKB_Excghp
from loader_kz_kkb_cards import Loader_KZ_KKB_cards
from loader_kz_bai_alfa import Loader_KZ_bai_alfa
import config


class Test_Loader:
    def setup(self):
        print("SETUP!")
        os.chdir("D:\\Boris\\Documents\\Projects\\Py\\tg_exchrates\\")
        print("work dir is", os.getcwd())

        self.kz_nb_ldr = Loader_KZ_NB()
        self.kz_kkber_ldr = Loader_KZ_KKB_Excghp()
        self.kz_kkbcrd_ldr = Loader_KZ_KKB_cards()
        self.kz_bai_alfa_ldr = Loader_KZ_bai_alfa()

    def teardown(self):
        print("TEAR DOWN!")

    def test_case1_KZ_NB_LoaderName(self):
        assert self.kz_nb_ldr.loader_name == config.RATE_SCR_KZ_NB

    def test_case1_KZ_NB_Loader_Parse(self):
        file = codecs.open("tests\\get_rates.cfm.nb.kz.xml", 'r', 'utf-8')
        dataForParse = file.read()

        assert self.kz_nb_ldr.parseDailyData(dataForParse) == [('KZ_NB', 0, 0, 351.77, datetime.datetime(2016, 2, 23, 0, 0), 'KZT', 
            'USD', 1), ('KZ_NB', 0, 0, 389.59, datetime.datetime(2016, 2, 23, 0, 0), 'KZT', 'EUR', 1), ('KZ_NB', 0, 0, 4.68, 
            datetime.datetime(2016, 2, 23, 0, 0), 'KZT', 'KGS', 1), ('KZ_NB', 0, 0, 4.63, datetime.datetime(2016, 2, 23, 0, 0), 'KZT', 
            'RUB', 1), ('KZ_NB', 0, 0, 498.6, datetime.datetime(2016, 2, 23, 0, 0), 'KZT', 'GBP', 1), ('KZ_NB', 0, 0, 354.14, 
            datetime.datetime(2016, 2, 23, 0, 0), 'KZT', 'CHF', 1)]

    def test_case1_KZ_KKBER_LoaderName(self):
        assert self.kz_kkber_ldr.loader_name == config.RATE_SCR_KZ_KKB_EXCHR

    def test_case1_KZ_KKBER_Loader_Parse(self):
        file = codecs.open("tests\\kkb_exch rates.html", 'r', 'utf-8')
        dataForParse = file.read()

        assert self.kz_kkber_ldr.parseDailyData(dataForParse) ==[('KZ_KKBER', 331.2, 325.2, 0, datetime.datetime(2017, 1, 25, 0, 0), 'KZT', 
            'USD', 1), ('KZ_KKBER', 355.85, 349.85, 0, datetime.datetime(2017, 1, 25, 0, 0), 'KZT', 'EUR', 1), ('KZ_KKBER', 5.69, 5.39, 0, 
            datetime.datetime(2017, 1, 25, 0, 0), 'KZT', 'RUB', 1), ('KZ_KKBER', 419.05, 407.05, 0, datetime.datetime(2017, 1, 25, 0, 0), 'KZT', 
            'GBP', 1), ('KZ_KKBER', 334.7, 322.7, 0, datetime.datetime(2017, 1, 25, 0, 0), 'KZT', 'CHF', 1)]

    def test_case1_KZ_KKBCRD_LoaderName(self):
        assert self.kz_kkbcrd_ldr.loader_name == config.RATE_SCR_KZ_KKB_CARDS

    def test_case1_KZ_KKBCRD_Loader_Parse(self):
        file = codecs.open("tests\\kkb_card_rates.html", 'r', 'utf-8')
        dataForParse = file.read()

        assert self.kz_kkbcrd_ldr.parseDailyData(dataForParse) == [['KZ_KKBCRD', 325.79, 330.46, 0, datetime.datetime(2017, 1, 29, 0, 0), 'KZT', 
        'USD', 1], ['KZ_KKBCRD', 346.84, 355.16, 0, datetime.datetime(2017, 1, 29, 0, 0), 'KZT', 'EUR', 1], ['KZ_KKBCRD', 5.344, 5.666, 0, 
        datetime.datetime(2017, 1, 29, 0, 0), 'KZT', 'RUB', 1], ['KZ_KKBCRD', 46.86, 48.83, 0, datetime.datetime(2017, 1, 29, 0, 0), 'KZT', 'CNY', 1]]

    def test_case1_KZ_bai_alfa_LoaderName(self):
        assert self.kz_bai_alfa_ldr.loader_name == config.RATE_SCR_KZ_ALFA

    def test_case1_KZ_bai_alfa_Loader_Parse(self):
        file = codecs.open("tests\\baikz alfa.html", 'r', 'utf-8')
        dataForParse = file.read()

        assert self.kz_bai_alfa_ldr.parseDailyData(dataForParse) == [['KZ_ALFA', 326.0, 328.0, 0, datetime.datetime(2017, 1, 30, 0, 0), 
        'KZT', 'USD', 1], ['KZ_ALFA', 347.5, 351.5, 0, datetime.datetime(2017, 1, 30, 0, 0), 'KZT', 'EUR', 1], ['KZ_ALFA', 5.38, 5.46, 0, 
        datetime.datetime(2017, 1, 30, 0, 0), 'KZT', 'RUB', 1]]

    def test_getting_currency_list_as_separate_function(self):
        currency_list = ['EUR', 'USD', 'RUB', 'CHF', 'GBP', 'KGS'] 
        loaded_currency_list = self.kz_nb_ldr.get_currency_list()
        assert set(loaded_currency_list) == set(currency_list)

    def test_getting_source_domain_as_separate_function(self):
        domain = 'nb.kz' 
        loaded_domain = self.kz_nb_ldr.get_domain()
        assert loaded_domain == domain


if __name__ == '__main__':
    nose.main()
