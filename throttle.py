# -*- coding: utf-8 -*-
import datetime
import time
import sqlite3

import config


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class Throttle:
	"""Add a delay between downloads to the same domain
	"""
	def __init__(self, delay):
		self.delay = delay
		self.connection = sqlite3.connect(config.dbname)
		self.cursor = self.connection.cursor()

		self.domains = {}
		#TODO: try
		sql_text = 'SELECT rs.DOMAIN, lg.LOAD_DATETIME ' \
						'from rates_sources rs, log_load lg ' \
						'where lg.SRC_ID = rs.ID and ' \
						'rs.ACTIVE = "True" '\
						'group by rs.DOMAIN'
		self.cursor.execute(sql_text)
		for row in self.cursor:
			self.domains[row[0]] = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
#			self.domains[row[0]] = datetime.datetime.fromtimestamp(row[1])
		logger.info(self.domains)	


	def wait(self, src_id):
		logger.info("we are in wait function for scr_id = " + src_id)

		sql_text = 'SELECT rs.DOMAIN from rates_sources rs where rs.ID = ? group by rs.DOMAIN' 
		self.cursor.execute(sql_text, (src_id,))

		for row in self.cursor:
			domain = row[0]

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
