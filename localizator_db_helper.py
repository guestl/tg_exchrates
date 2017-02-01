# -*- coding: utf-8 -*-

# helper for work with database for localizator
import sqlite3

import config

import logging

logger = logging.getLogger(__name__)

class db_localizator_helper:
	"""class helper for work with SQLite3 database
		for localizator only
	
	
	methods:
		__init__ -- setup db setting
		check_lang_id -- check if language is in DB or not
		get_labels_list -- get list of labels and receive list of translated labels from DB
	"""
	def __init__(self, dbname = config.dbname):
		self.dbname = dbname
		self.connection = sqlite3.connect(dbname)
		self.cursor = self.connection.cursor()

	def check_lang_id(self, lang_id):
		sql_text = "SELECT count(ID) from lang where id = ?"
		self.cursor.execute(sql_text, (lang_id, ))
		fetched_data = self.cursor.fetchall()

		for item in fetched_data:
			if item[0] > 0: 
				return True
		return False	

	def get_labels_list(self, lang_id, data_list):
		result = []
		
		for item in data_list:
			# is item type string?
			if isinstance(item, str):
				if item.find(config.label_id) > -1:
					sql_text = "SELECT TEXT from labels where LABEL_ID = ? and LANG_ID = ?"
					self.cursor.execute(sql_text, (item, lang_id))
					fetched_data = self.cursor.fetchall()

					if len(fetched_data) > 0:
					# we find anything in DB	
						for row in fetched_data:
							result.append(row[0])
					else:
						#found nothing in DB
						result.append(item)		
				else:
					#found nothing is item
					result.append(item)
			else:
				#it is not a string
				result.append(item)
		return result