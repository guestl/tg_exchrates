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
	def __init__(self, loader_name, return_list, currency_list,  *args, **kwargs):
		self.inTable = False
		self.inRow = False
		self.skip_text_counter = 0
		self.pair_counter = 0
		self.curList = currency_list
		self.cur_index = 0
		self.return_list = return_list
		self.loader_name = loader_name
		self.cur_date = None
		self.buy_v = 0
		self.sell_v = 0
		self.avr_v = 0
		self.quant = 1
		self.date_first_index = 5
		self.date_second_index = 1

		self.date_text = 'data'
		self.date_attrs_len = 6
		self.tbl_text = 'tbl_text90'
		super().__init__(*args, **kwargs)

	def handle_starttag(self, tag, attrs):
		if tag == 'input' and attrs[0][1] == self.date_text and len(attrs) == self.date_attrs_len:
			try:
				self.cur_date = datetime.strptime(attrs[self.date_first_index][self.date_second_index], "%d.%m.%Y")
			except Exception as e:
				logger.error("Error while converting date")
				logger.error(e)
				self.cur_date = None
		if tag == 'table' and len(attrs) == 3:
			if attrs[2][1] == self.tbl_text:
				self.inTable = True
		if tag == 'tbody' and len(attrs) == 1:
			if attrs[0][1] == 'font-weight: bold;':
				self.inRow = True

	def handle_endtag(self, tag):
		if tag == 'table' and self.inTable:
			self.inTable = False
			self.inRow = False
		if tag == 'tbody' and self.inRow:
			self.inTable = True
			self.inRow = False

	def handle_data(self, data):
		if self.inRow and self.skip_text_counter < 1:
			self.skip_text_counter += 1
		elif self.inRow and self.skip_text_counter == 1:	
			if self.pair_counter == 0:
				try:
					self.buy_v = float(data)
				except Exception as e:
					logger.error(e)
					self.buy_v = None
			self.pair_counter += 1
			if self.pair_counter > 1:
				try:
					self.sell_v = float(data)
				except Exception as e:
					logger.error(e)
					self.sell_v = None
				self.return_list.append([self.loader_name, self.buy_v, self.sell_v, self.avr_v, self.cur_date, config.CUR_KZT, 
					self.curList[self.cur_index], self.quant])
				self.pair_counter = 0
				self.cur_index += 1
	


class Loader_KZ_KKB_cards(loader_default):
	"""Load and parse data from KKB (exchange points)
	
	methods:
		loadDailyData - load rates data for a specific date
		parseDailyData - parse loaded rates data
		saveRatesData - save parsed data to database
	"""

	def __init__(self, loader_name = config.RATE_SCR_KZ_KKB_CARDS):
		self.url = 'http://www.kkb.kz/rates/RatesCards.jsp'

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
		self.daily_date = dateForLoad.date()
		str_date_for_load = self.daily_date.strftime('%d.%m.%Y')

		# temporary get data from a file
		loadedData = ''

		try:
			req = requests.post(self.url, data = {'data':str_date_for_load}, headers = self.headers)
			loadedData = req.text

			self.update_loader_log(self.loader_name)
		except Exception as e:
			logger.error("Error during loading process")
			logger.error(e)
			loadedData = None

		if loadedData:
			self.saveCachedData(loadedData)
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

#		cur_list = self.database.get_currency_list(self.loader_name)
# because of strict order
#TODO: попробовать переделать
		cur_list = [config.cur_usd, config.cur_eur, config.cur_rub, config.cur_cny]

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