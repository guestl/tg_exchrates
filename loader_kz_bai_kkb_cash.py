# -*- coding: utf-8 -*-

import config

from loader_def_kz_bai import Loader_def_KZ_bai

import logging

logger = logging.getLogger(__name__)
logger.setLevel(config.LOGGER_LEVEL)


class Loader_KZ_bai_kkb_cash(Loader_def_KZ_bai):
    """Load and parse data from KKB (exchange points)
    methods:
        loadDailyData - load rates data for a specific date
        parseDailyData - parse loaded rates data
        saveRatesData - save parsed data to database
    """

    def __init__(self, loader_name=config.RATE_SCR_KZ_KKB_CASH):
        self.url = 'http://bai.kz/bank/kazkom/kursy/'

        super().__init__(loader_name, self.url)
