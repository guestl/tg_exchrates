# -*- coding: utf-8 -*-

# helper for work with database
import config

from loader_def_kz_bai import Loader_def_KZ_bai

#from datetime import datetime
#from html.parser import HTMLParser
#import requests
#import codecs

import logging
#import loader_db_helper

logger = logging.getLogger(__name__)
logger.setLevel(config.LOGGER_LEVEL)


class Loader_KZ_bai_halyk_cards(Loader_def_KZ_bai):
    """Load and parse data from halyk (exchange points)

    methods:
        loadDailyData - load rates data for a specific date
        parseDailyData - parse loaded rates data
        saveRatesData - save parsed data to database
    """

    def __init__(self, loader_name=config.RATE_SCR_KZ_HALYK_CARDS):
        self.url = 'http://bai.kz/bank/narodnyi-bank/kursy/'

        super().__init__(loader_name, self.url)
