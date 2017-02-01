# -*- coding: utf-8 -*-

# helper for work with database
import config

from loader_def_class import loader_default

from datetime import datetime
from html.parser import HTMLParser
import requests
import codecs

import logging
import loader_db_helper

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class MyHTMLParser(HTMLParser):
	def __init__(self, loader_name, return_list, currency_list, *args, **kwargs):
		self.inTable = False
		self.inRow = False
		self.inCurRow = False
		self.counter = -1

		self.currency_attrs_len = 7
		self.currency_attrs_name = 'repayment-table'
		self.curr_id_position = 0
		self.buy_v_position = 1
		self.sell_v_position = 2
		self.date_first_index = 4
		self.date_second_index = 1


		self.return_list = return_list
		self.rate_date = None
		self.cur_id_to = None
		self.loader_name = loader_name
		self.buy_value = 0
		self.sell_value = 0
		self.avrg_value = 0
		self.quant = 1
		self.curList = currency_list
		
		super().__init__(*args, **kwargs)

	def handle_starttag(self, tag, attrs):
		if tag == 'input' and attrs[0][1] == 'text' and len(attrs) == self.currency_attrs_len:
			#TODO: try	
			self.rate_date = datetime.strptime(attrs[self.date_first_index][self.date_second_index], "%d.%m.%Y")
		if tag == 'table':
			if attrs[0][1] == self.currency_attrs_name:
				self.inTable = True
		if tag == 'tr' and self.inTable:
			self.inRow = True

	def handle_endtag(self, tag):
		if tag == 'table' and self.inTable:
			self.inTable = False
			self.inRow = False
		if tag == 'tr' and self.inTable:
			self.inTable = True
			self.inRow = False
			self.inCurRow = False
			self.counter = -1

	def handle_data(self, data):
		if self.inRow and data in self.curList:
			self.inCurRow = True
		if self.inCurRow:
			self.counter += 1
		if self.counter == self.curr_id_position:
			self.cur_id_to = data
		#TODO: try	
		if self.counter == self.buy_v_position:
			self.buy_value = float(data)
		#TODO: try	
		if self.counter == self.sell_v_position:
			self.sell_value = float(data)
			#because it is the last value we add all collected data in return list
			self.return_list.append((self.loader_name, self.buy_value, self.sell_value, self.avrg_value, 
					self.rate_date, config.CUR_KZT, self.cur_id_to, self.quant))

class Loader_KZ_KKB_Excghp(loader_default):
	"""Load and parse data from KKB (exchange points)
	
	methods:
		loadDailyData - load rates data for a specific date
		parseDailyData - parse loaded rates data
		saveRatesData - save parsed data to database
	"""

	def __init__(self, loader_name = config.RATE_SCR_KZ_KKB_EXCHR):
		self.url = 'http://www.kkb.kz/rates/RatesExch.jsp'

		super().__init__(loader_name)

	def loadDailyData(self, dateForLoad):
		"""Download daily currency exchange rates data from specific url
		
		Arguments:
			dateForLoad {Date} -- [Date for load]
		
		Returns:
			[string] -- [return context of web page with exchange rates or 'None']
		"""
		logger.info("load Daily Data for date")
		logger.info(dateForLoad.date())
		self.dailyData = dateForLoad.date()
		str_date_for_load = self.dailyData.strftime('%d.%m.%Y')

		# temporary get data from a file
		loadedData = ''

		try:
			req = requests.post(self.url, data = {'name':'form2', 'date':str_date_for_load}, headers = self.headers)
			loadedData = req.text

			self.update_loader_log(self.loader_name)
		except Exception as e:
			logger.error("Error during loading process")
			logger.error(e)
			loadedData = None

		if loadedData:
			return loadedData
		else: return None


	def parseDailyData(self, dataForParse):
		"""Parse downloaded data
		
		Arguments:
			dataForParse {string} -- [String with data for parsing]

		Returns:
			[list] -- [return list of specific data (source, avrg_value, rate_datetime, curidfrom, curidto, quant) or 'None']
		"""
		logger.info("we have to parse for these currencies:")

		#setup default values
		quant = 1

		return_list = []

		cur_list = self.get_currency_list()

		logger.info(cur_list)

		parser = MyHTMLParser(self.loader_name, return_list, cur_list)

		parser.feed(dataForParse)
		parser.close()


		logger.info(return_list)
		if return_list:
			return return_list
		return None

	def saveRatesData(self, parsedData):
		logger.info("We will ask to insert the next data:")
		logger.info(parsedData)
		super().saveRatesData(parsedData)