# -*- coding: utf-8 -*-

# run me in windows as python loader_main.py -d (Get-Date -Year 2017 -Month 01 -Day 11 -UFormat "%d/%m/%Y")


import logging
import logging.config
import datetime
import argparse

import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import config
from throttle import Throttle

from loader_kz_nb import Loader_KZ_NB
from loader_kz_bai_alfa import Loader_KZ_bai_alfa
from loader_kz_bai_halyk_cash import Loader_KZ_bai_halyk_cash
from loader_kz_bai_halyk_cards import Loader_KZ_bai_halyk_cards
from loader_kz_bai_kkb_cash import Loader_KZ_bai_kkb_cash
from loader_kz_bai_kkb_cards import Loader_KZ_bai_kkb_cards

#from localizator import localizator

logging.config.fileConfig('logging_loader.ini', disable_existing_loggers=False)

logger = logging.getLogger()  # this gets the root logger
logger.setLevel(config.LOGGER_LEVEL)

# parse command line parameters
parser = argparse.ArgumentParser(description='Exchange rates loader main script')

parser.add_argument('-d', help="Date in format dd/mm/YYYY. If empty the script will use current date", required=False)

args = parser.parse_args()

# logging.info("args is: ")
# logging.info(args)


date_for_load = datetime.datetime.now()
if args.d:
    try:
        args_date = datetime.datetime.strptime(args.d, "%d/%m/%Y")
        # logging.debug("args date is: ")
        # logging.debug(args_date)
        date_for_load = args_date
    except Exception as e:
        logging.error("Invalid command line parameter:")
        logging.error(args)
        logging.error(e)
        date_for_load = datetime.datetime.now()

# init delay
throttle = Throttle(config.delay)

# create new loader instance
ldr_kz_nb = Loader_KZ_NB()
ldr_kz_bai_alfa = Loader_KZ_bai_alfa()
kz_bai_halyk_cash_ldr = Loader_KZ_bai_halyk_cash()
kz_bai_halyk_cards_ldr = Loader_KZ_bai_halyk_cards()
kz_bai_kkb_cash_ldr = Loader_KZ_bai_kkb_cash()
kz_bai_kkb_cards_ldr = Loader_KZ_bai_kkb_cards()

# here is the place for adding an instance into the loaders list
loaders_list = [ldr_kz_nb, ldr_kz_bai_alfa, kz_bai_halyk_cash_ldr, kz_bai_halyk_cards_ldr,
                kz_bai_kkb_cash_ldr, kz_bai_kkb_cards_ldr]


loadedData = ''
# loop in loaders list
for ldr in loaders_list:
    loadedData = ldr.loadDailyData(date_for_load)
    if loadedData:
        parsedData = ldr.parseDailyData(loadedData)
    else:
        logging.error("Empty loaded data")
        parsedData = None

    if parsedData:
        ldr.saveRatesData(parsedData)
    throttle.wait(ldr.get_domain())

# loc = localizator("en-us")

# logging.info(loc.get_translated_labels(["EUR","LBL000002", 12.4,"LBL000001", "LBL000005"]))
