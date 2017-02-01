# -*- coding: utf-8 -*-

# helper for work with database
import config
import loader_db_helper
from loader_def_class import loader_default

import io
from lxml import etree
from datetime import datetime
import requests

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class Loader_def_KZ_bai(loader_default):
	"""Load and parse data from bai.kz
	
	methods:
		loadDailyData - load rates data for a specific date
		parseDailyData - parse loaded rates data
		saveRatesData - save parsed data to database
	"""

	def __init__(self, loader_name, url):
		super().__init__(loader_name)
		self.url = url
		self.loader_name = loader_name

	def loadDailyData(self, dateForLoad):
		"""Download daily currency exchange rates data from specific url
		
		Arguments:
			dateForLoad {Date} -- [Date for load]
		
		Returns:
			[string] -- [return context of web page with exchange rates or 'None']
		"""
#		logger.info("load Daily Data for date")
#		logger.info(dateForLoad.date())
		self.dailyData = dateForLoad.date()
		str_date_for_load = self.dailyData.strftime('%d.%m.%Y')

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
			return loadedData
		else: return None


	def parseDailyData(self, dataForParse):
		"""Parse downloaded data
		
		Arguments:
			dataForParse {string} -- [String with data for parsing]

		Returns:
			[list] -- [return list of specific data (source, avrg_value, rate_datetime, curidfrom, curidto, quant) or 'None']
		"""
#		logger.info("we have to parse for these currencies:")

		#setup default values
		quant = 1

		return_list = []
		currency_dict = {}

		cur_list = self.get_currency_list()

#		logger.info(cur_list)

		parser = etree.HTMLParser()
		tree = etree.parse(io.StringIO(dataForParse),parser)

		elements = tree.xpath('//table[@class="cv_table"]/tbody/tr/th/div/following-sibling::text()')
		idx = 0

		for i in elements:
			parsed_cur = ''.join(i.split())
			return_list.append([self.loader_name , 0, 0, 0, None, config.CUR_KZT, 
						parsed_cur, quant])
			currency_dict[parsed_cur] = [idx, parsed_cur in cur_list]
			idx += 1

		idx = 0

		row_count = int(tree.xpath('count(//table[@class="cv_table"]/tbody/tr)'))
	
		for i in range(2, row_count + 1):
			rows = tree.xpath('//table[@class="cv_table"]/tbody/tr[' + str(i) + ']')
			for row in rows:
				#TODO: try
				td = row.xpath('./td[1]')
				return_list[idx][7] = int(td[0].text)
				td = row.xpath('./td[3]')
				return_list[idx][1] = float(td[0].text)
				td = row.xpath('./td[4]')
				return_list[idx][2] = float(td[0].text)
				td = row.xpath('./td[5]')
				return_list[idx][4] =  datetime.strptime(td[0].text, "%d.%m.%Y")
			idx += 1

		for cur_el in currency_dict:
			for res_el in return_list:
				if cur_el == res_el[6] and not currency_dict.get(cur_el)[1]:
					return_list.remove(res_el)
					break

#		logger.info(return_list)
		if return_list:
			return return_list
		return None

	def saveRatesData(self, parsedData):
#		logger.info("We will ask to insert the next data:")
#		logger.info(parsedData)
		super().saveRatesData(parsedData)