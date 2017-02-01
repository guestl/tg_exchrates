# -*- coding: utf-8 -*-
import datetime
import time
import sqlite3

import config

from loader_def_class import loader_default

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class Throttle:
	"""Add a delay between downloads to the same domain
	"""

	def __init__(self, delay):
		self.delay = delay

		# it is not well solution, I agree
		self.ldr_default = loader_default('')

		self.domains = self.ldr_default.get_domains_history()

		logger.info(self.domains)	


	def wait(self, domain):
		logger.info("we are in wait function for scr_id = " + domain)

		logger.info("Domain is " + domain)	

		last_access = self.domains.get(domain)

		utc_dt = datetime.datetime.utcfromtimestamp(time.time())
		logger.info("last_access is ")
		logger.info(last_access)
		logger.info("now is ")
		logger.info(utc_dt)

		if self.delay > 0 and last_access is not None:
			sleep_secs = self.delay - (utc_dt - last_access).seconds

			if sleep_secs > 0:
				logger.info("we are waiting for:")
				logger.info(sleep_secs)
				time.sleep(sleep_secs)

			self.domains[domain] = utc_dt
