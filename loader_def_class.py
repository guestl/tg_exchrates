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

		self.user_agent = config.USER_AGENTS[random.randrange(len(config.USER_AGENTS))]
		self.headers = {'user-agent' : self.user_agent}

	@abstractmethod
	# empty method
	def loadDailyData(self, dateForLoad):
		pass

	@abstractmethod
	# empty method
	def set_currency_list(self, currency_list):
		pass

	def get_currency_list(self):
		return self.database.get_currency_list(self.loader_name)

	def get_domain(self):
		return self.database.get_domain(self.loader_name)

	def get_domains_history(self):
		return self.database.get_domains_history()

	#TODO: переделать. убрать scr_id, он и так у нас уже есть
	def update_loader_log(self, src_id):
		self.database.update_loader_log(src_id)	

	@abstractmethod
	# empy method
	def parseDailyData(self, dataForParse):
		pass

	# save parsed data into db
	def saveRatesData(self, parsedData):
		self.database.add_currency_rates_data(parsedData)