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

    def bf_set_user_setting(self, uid):
        pass

    def bf_get_user_setting(self):
        pass
