from loader_db_helper import db_loader_helper
from abc import ABCMeta, abstractmethod
import config
import random

class loader_default:

	__metaclass__ = ABCMeta

	#init db connection
	def __init__(self, loader_name):
		self.database = db_loader_helper()
		self.loader_name = loader_name

		self.user_agent = config.user_agents[random.randrange(len(config.user_agents))]
		self.headers = {'user-agent' : self.user_agent}

	@abstractmethod
	# empty method
	def loadDailyData(self, dateForLoad):
		pass

	def update_loader_log(self, src_id):
		self.database.update_loader_log(src_id)	

	@abstractmethod
	# empy method
	def parseDailyData(self, dataForParse):
		pass

	# save parsed data into db
	def saveRatesData(self, parsedData):
		self.database.add_currency_rates_data(parsedData)