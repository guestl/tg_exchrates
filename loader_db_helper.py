# -*- coding: utf-8 -*-

# helper for work with database
import sqlite3

import config

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class db_loader_helper:
	"""class helper for work with SQLite3 database
	
	
	methods:
		__init__ -- setup db setting
		add_currency_rates_data -- insert parsed data into rates table
	"""
	def __init__(self, dbname = config.dbname):
#		logger.info("init db helper class")
		self.dbname = dbname
		self.connection = sqlite3.connect(dbname)
		self.cursor = self.connection.cursor()

	def get_countries_list(self):
		result = []
		sql_text = "SELECT ID, NAME, C.ID from state as s, currency as c where s.CUR_ID_FROM = C.ID"
		self.cursor.execute(sql_text, (src_id, ))
		for row in self.cursor:
			result.append(row[0])
		return result 
		
	def get_languages_list(self):
		result = []
		sql_text = "SELECT ID, TEXT from lang"
		self.cursor.execute(sql_text)
		for row in self.cursor:
			result.append(row[0])
		return result 
				
	def get_currency_list(self, src_id):
		result = []
#		sql_text = "SELECT CUR_ID from ref_src_cur where SRC_ID = ?"
		sql_text = "SELECT r.CUR_ID from ref_src_cur r, rates_sources as s where r.SRC_ID = ? and s.ID = r.src_id and s.ACTIVE = 'True'"
		self.cursor.execute(sql_text, (src_id, ))
		for row in self.cursor:
			result.append(row[0])
		return result 

	#TODO: проверить, если на входе один список, а не список списков
	def add_currency_rates_data(self, parsed_data):
		logger.info("add_currency_rates_data -> parsed data is ")
		logger.info(parsed_data)
		
		#TODO: try
		sql_text = "REPLACE INTO rates (SRC_ID, BUY_VALUE, SELL_VALUE, AVRG_VALUE, RATE_DATETIME, CUR_ID_FROM, CUR_ID_TO, QUANT) VALUES (?,?,?,?,?,?,?,?)"
		self.connection.executemany(sql_text, parsed_data)
		self.connection.commit()

		logger.info("Commit done")

	def update_loader_log(self, src_id):

		logger.info("add_loader log data for source ")
		logger.info(src_id)
		
		#TODO: try
		sql_text = "INSERT INTO log_load (SRC_ID) VALUES (?)"
		self.connection.execute(sql_text, (src_id,))
		self.connection.commit()

		logger.info("Commit done")
