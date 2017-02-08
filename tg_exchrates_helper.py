# -*- coding: utf-8 -*-

import tg_token
import config
from tg_exchrates_db_helper import db_tg_exchrates_helper
from localizator import localizator

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class tg_exchrates_helper:
    def __init__(self, token=tg_token.token):
        self.token = token
        self.def_state = config.DEF_STATE
        self.def_lang = config.DEF_LANG
        self.def_currency_list = config.DEF_CURRENCIES_LIST

        self.database = db_tg_exchrates_helper()
        self.loc = localizator("en-us")
        # logging.info(loc.get_translated_labels(["EUR","LBL000002", 12.4,"LBL000001", "LBL000005"]))

    def bf_generate_user_data(self, s_UID):
        user_data = []

        for i in range(config.DEF_SETTINGS_COUNT):
            def_set = [s_UID]
            for elem in config.DEF_USER_SETTING:
                def_set.append(elem)
            user_data.append(def_set)

        return user_data

    def bf_create_new_user(self, s_UID):
        def_data = self.bf_generate_user_data(s_UID)
        self.database.create_new_user(def_data)

    def bf_set_active_settings_set(self, s_UID, set_nmb):
        pass

    def bf_get_user_set_lst(self, s_UID):
        pass

    def bf_save_user_set_lst(self, s_UID, set_lst_nmb):
        pass

    def bf_set_user_set_lst_1(self, s_UID, set_lst_nmb):
        pass

    def bf_set_user_setting(self, s_UID):
        pass

    def bf_get_user_setting(self, s_UID):
        pass
