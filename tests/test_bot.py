# run me as "nosetests -v --with-coverage --cover-inclusive --cover-package="tg_exchrates""
from nose.tools import *

import os
# import sys
# import io
import codecs
import datetime

import config
from tg_exchrates_helper import tg_exchrates_helper


class Test_Bot:
    @classmethod
    def setup_class(self):
        print("Setup class test_bot!")
        os.chdir("D:\\Boris\\Documents\\Projects\\Py\\tg_exchrates\\")
        print("work dir is", os.getcwd())

        self.tg_helper = tg_exchrates_helper()
        self.test_uid = 'test_UID'

    @classmethod
    def teardown_class(self):
        print("Tear down class test_bot!")

    def test_generation_of_default_user_data(self):
        def_data = [[self.test_uid, config.DEF_LANG, config.DEF_STATE, config.RATE_SCR_KZ_NB, config.DEF_CURRENCIES_LIST],
                    [self.test_uid, config.DEF_LANG, config.DEF_STATE, config.RATE_SCR_KZ_NB, config.DEF_CURRENCIES_LIST],
                    [self.test_uid, config.DEF_LANG, config.DEF_STATE, config.RATE_SCR_KZ_NB, config.DEF_CURRENCIES_LIST]]

        gen_data = self.tg_helper.bf_generate_user_data(self.test_uid)
        assert gen_data == def_data

    def test_get_def_settings_for_user(self):
        self.tg_helper.bf_set_user_setting(self.test_uid)
        assert self.tg_helper.bf_get_user_setting(self.test_uid) == [self.test_uid, config.DEF_STATE,
                                                                     config.DEF_LANG, config.RATE_SCR_KZ_NB,
                                                                     config.DEF_CURRENCIES_LIST]


if __name__ == '__main__':
    nose.main()
