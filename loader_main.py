# -*- coding: utf-8 -*-

# run me as python loader_main.py -d (Get-Date -Year 2017 -Month 01 -Day 11 -UFormat "%d/%m/%Y")

# helper for work with database
import config
from throttle import Throttle

from loader_kz_nb import Loader_KZ_NB
from loader_kz_kkb_exchp import Loader_KZ_KKB_Excghp
from loader_kz_kkb_cards import Loader_KZ_KKB_cards
from loader_kz_bai_alfa import Loader_KZ_bai_alfa
from localizator import localizator

import logging
import logging.config
#from datetime import datetime
import datetime
import argparse

logging.config.fileConfig('logging_loader.ini', disable_existing_loggers=False)

logger = logging.getLogger() # this gets the root logger
logger.setLevel(logging.INFO)

#parse command line parameters
parser = argparse.ArgumentParser(description='Exchange rates loader main script')

parser.add_argument('-d', help = "Date in format dd/mm/YYYY. If empty the script will use current date", required = False)

args = parser.parse_args()

#logging.info("args is: ")
#logging.info(args)


date_for_load = datetime.datetime.now()
if args.d:
	try:
		args_date = datetime.datetime.strptime(args.d, "%d/%m/%Y")
		logging.info("args date is: ")
		logging.info(args_date)
		date_for_load = args_date
	except Exception as e:
		logging.error("Invalid command line parameter:")
		logging.error(args)
		logging.error(e)
		date_for_load = datetime.datetime.now()

#init delay 
throttle = Throttle(config.delay)

#create new loader instance
ldr_kz_nb = Loader_KZ_NB()
ldr_kz_kkb_exchp = Loader_KZ_KKB_Excghp()
ldr_kz_kkb_cards = Loader_KZ_KKB_cards()
ldr_kz_bai_alfa = Loader_KZ_bai_alfa()

#here is the place for adding an instance into the loaders list
loaders_list = [ldr_kz_nb, ldr_kz_kkb_exchp, ldr_kz_kkb_cards, ldr_kz_bai_alfa]


loadedData = ''
#loop in loaders list
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

#loc = localizator("en-us")

#logging.info(loc.get_translated_labels(["EUR","LBL000002", 12.4,"LBL000001", "LBL000005"]))