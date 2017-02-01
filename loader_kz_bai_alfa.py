# -*- coding: utf-8 -*-

# helper for work with database
import config

from loader_def_kz_bai import Loader_def_KZ_bai

from datetime import datetime
from html.parser import HTMLParser
import requests
import codecs

import logging
import loader_db_helper

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


class Loader_KZ_bai_alfa(Loader_def_KZ_bai):
	"""Load and parse data from KKB (exchange points)
	
	methods:
		loadDailyData - load rates data for a specific date
		parseDailyData - parse loaded rates data
		saveRatesData - save parsed data to database
	"""

	def __init__(self, loader_name = config.RATE_SCR_KZ_ALFA):
		self.url = 'http://bai.kz/bank/alfa-bank/kursy/'

		super().__init__(loader_name, self.url)

	def loadDailyData(self, dateForLoad):
		"""Download daily currency exchange rates data from specific url
		
		Arguments:
			dateForLoad {Date} -- [Date for load]
		
		Returns:
			[string] -- [return context of web page with exchange rates or 'None']
		"""
		return super().loadDailyData(dateForLoad)


	def parseDailyData(self, dataForParse):
		"""Parse downloaded data
		
		Arguments:
			dataForParse {string} -- [String with data for parsing]

		Returns:
			[list] -- [return list of specific data (source, avrg_value, rate_datetime, curidfrom, curidto, quant) or 'None']
		"""
		return super().parseDailyData(dataForParse)

	def saveRatesData(self, parsedData):
		logger.info("We will ask to insert the next data:")
		logger.info(parsedData)
		super().saveRatesData(parsedData)