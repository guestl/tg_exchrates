# -*- coding: utf-8 -*-

# helper for work with database
import config

from loader_def_class import loader_default

from datetime import datetime
import xml.etree.ElementTree as etree
import requests
import logging
import loader_db_helper

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


class Loader_KZ_NB(loader_default):
	"""Load and parse data from National bank of Kazakhstan
	
	methods:
		loadDailyData - load rates data for a specific date
		parseDailyData - parse loaded rates data
		saveRatesData - save parsed data to database
	"""

	def __init__(self, loader_name = config.RATE_SCR_KZ_NB):
		self.url = 'http://www.nationalbank.kz/rss/get_rates.cfm?fdate='

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

		# temporary get data from a file
		loadedData = ''


		try:
			req = requests.get(self.url + dateForLoad.strftime("%d.%m.%Y"), headers = self.headers)
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
		buy_value = 0
		sell_value = 0
		avrg_value = 0
		cur_id_to = ''
		quant = 0

		cur_list = self.get_currency_list()

		logger.info(cur_list)

		root = etree.fromstring(dataForParse)

		rate_date = datetime.strptime(root.findall('.//date')[0].text, "%d.%m.%Y")

		return_list = []

		items = root.findall('.//item')
		for i in items:
			dat = list(i)
			if dat[1].text not in cur_list:
				continue

			try:
				avrg_value = float(dat[2].text)
				cur_id_to = dat[1].text
				quant = int(dat[3].text)

				return_list.append((self.loader_name, buy_value, sell_value, avrg_value, 
					rate_date, config.CUR_KZT, cur_id_to, quant))
			except Exception as e:
				logger.error("Error during parse process")
				logger.error(e)
				avrg_value = 0
				cur_id_to = None
				quant = None


		logger.info(return_list)
		if return_list:
			return return_list
		return None

	def saveRatesData(self, parsedData):
		logger.info("We will ask to insert the next data:")
		logger.info(parsedData)

		super().saveRatesData(parsedData)