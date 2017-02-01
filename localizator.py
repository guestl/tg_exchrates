# -*- coding: utf-8 -*-

# helper for work with localization
import config

import logging
import localizator_db_helper 

class localizator:
	#default language
	language = config.def_lang
	database = None

	def __init__(self, language):
		self.database = localizator_db_helper.db_localizator_helper()

		if self.check_lang_id(language):
			self.language = language
		else:
			self.language = config.def_lang


	def check_lang_id(self, language):
		return self.database.check_lang_id(language)

	def get_translated_labels(self, data_list):
		return self.database.get_labels_list(self.language, data_list)

