# -*- coding: utf-8 -*-

# helper for work with database
import sqlite3

import config

import logging
import datetime
import os


logger = logging.getLogger(__name__)
logger.setLevel(config.LOGGER_LEVEL)

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class db_tg_exchrates_helper:
    """class helper for work with SQLite3 database

    methods:
        __init__ -- setup db setting
        add_currency_rates_data -- insert parsed data into rates table
    """
    def __init__(self, dbname=config.dbname):
        self.dbname = dbname
        try:
            self.connection = sqlite3.connect(dbname)
            self.cursor = self.connection.cursor()
        except Exception as e:
            logger.error(e)
            raise e

    # I got this piece of code from
    #    http://stackoverflow.com/questions/5266430/how-to-see-the-real-sql-query-in-python-cursor-execute"
    # it doesn't work pretty good, but I can see a sql text and it's enough for me
    def check_sql_string(self, sql_text, values):
        unique = "%PARAMETER%"
        sql_text = sql_text.replace("?", unique)
        for v in values:
            sql_text = sql_text.replace(unique, repr(v), 1)
        return sql_text
    """
    def get_countries_list(self):
        result = []
        try:
            sql_text = "SELECT ID, NAME, C.ID from state as s, currency as c where s.CUR_ID_FROM = C.ID"
            self.cursor.execute(sql_text)
        except Exception as e:
            logger.error(e)
            logger.error(sql_text)

        if self.cursor:
            for row in self.cursor:
                result.append(row[0])
        return result
    """

    def get_rate_src_type_string(self, src_id):
        """Get rate sources type for specific source

        Get type of rate source - cash rate or cards rate. We will compare these values with dict config.RATES_TYPES

        Returns:
            list -- list of IDX_TYPE fields from "global_variables" table
        """
        result = ''
        # logger.debug(src_id)

        try:
            sql_text = 'select gv.IDX_TYPE  ' \
                       'from global_variables gv, rates_sources rs ' \
                       'where rs.RATE_TYPE = gv.IDX_TYPE and ' \
                       'rs.ID = ?'
            self.cursor.execute(sql_text, (src_id, ))
        except Exception as e:
            logger.error(e)
            logger.error(sql_text)

        if self.cursor:
            for row in self.cursor:
                # logger.debug(row)
                result = row[0]
        return result

    def get_languages_list(self):
        result = []

        try:
            sql_text = "select ID, TEXT from lang"
            self.cursor.execute(sql_text)
        except Exception as e:
            logger.error(e)
            logger.error(sql_text)

        if self.cursor:
            for row in self.cursor:
                result.append(row[0])
        return result

    def get_currency_list(self, src_id):
        result = []

        try:
            sql_text = "select r.CUR_ID from ref_src_cur r, rates_sources as s " \
                       " where r.SRC_ID = ? and s.ID = r.src_id and s.ACTIVE = 'True'"
            self.cursor.execute(sql_text, (src_id, ))
        except Exception as e:
            logger.error(e)
            logger.error(self.check_sql_string(sql_text, (src_id, )))

        if self.cursor:
            for row in self.cursor:
                result.append(row[0])
        return result

    def get_domain(self, src_id):
        domain = None

        try:
            sql_text = 'select rs.DOMAIN from rates_sources rs where rs.ID = ? group by rs.DOMAIN'
            self.cursor.execute(sql_text, (src_id,))
        except Exception as e:
            logger.error(e)
            logger.error(self.check_sql_string(sql_text, (src_id, )))

        if self.cursor:
            for row in self.cursor:
                domain = row[0]

        return domain

    def get_domains_history(self):
        domains = {}

        try:
            sql_text = 'select rs.DOMAIN, lg.LOAD_DATETIME ' \
                       'from rates_sources rs, log_load lg ' \
                       'where lg.SRC_ID = rs.ID and ' \
                       'rs.ACTIVE = "True" '\
                       'group by rs.DOMAIN'
            self.cursor.execute(sql_text)
        except Exception as e:
            logger.error(e)
            logger.error(sql_text)

        if self.cursor:
            for row in self.cursor:
                domains[row[0]] = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')

        return domains

    # TODO: проверить, если на входе один список, а не список списков
    def add_currency_rates_data(self, parsed_data):
        logger.debug("add_currency_rates_data -> parsed data is ")
        logger.debug(parsed_data)

        try:
            sql_text = "REPLACE INTO rates (SRC_ID, BUY_VALUE, SELL_VALUE, AVRG_VALUE, " \
                       "RATE_DATETIME, CUR_ID_FROM, CUR_ID_TO, QUANT) VALUES (?,?,?,?,?,?,?,?)"
            self.connection.executemany(sql_text, parsed_data)

            self.connection.commit()
        except Exception as e:
            logger.error(e)
            logger.error(sql_text)
            logger.error(parsed_data)

        logger.debug("Commit done")

    def update_loader_log(self, src_id):

        logger.debug("add_loader log data for source ")
        logger.debug(src_id)

        try:
            sql_text = "INSERT INTO log_load (SRC_ID) VALUES (?)"
            self.connection.execute(sql_text, (src_id,))

            self.connection.commit()
        except Exception as e:
            raise e
            logger.error(self.check_sql_string(sql_text, (src_id, )))

        logger.debug("Commit done")

    def add_cache(self, data_for_cache):
        try:
            sql_text = "REPLACE INTO cache_rates (SRC_ID, REQUESTED_RATE_DATE, CACHE_DATA) VALUES (?,?,?)"
            self.connection.executemany(sql_text, (data_for_cache,))

            self.connection.commit()
        except Exception as e:
            logger.error(e)
            logger.error(sql_text)
            logger.error(data_for_cache)

        logger.debug("Commit done")

    def check_and_load_cache(self, src_id, req_date):
        try:
            sql_text = 'select cr.CACHE_DATA, cr.CACHE_DATETIME ' \
                       'from cache_rates cr ' \
                       'where cr.SRC_ID = ? and ' \
                       'cr.REQUESTED_RATE_DATE = ? ' \
                       'order by cr.CACHE_DATETIME desc ' \
                       'limit 1'
            self.cursor.execute(sql_text, (src_id, req_date, ))
        except Exception as e:
            logger.error(e)
            logger.error(self.check_sql_string(sql_text, (src_id, req_date, )))

        row = self.cursor.fetchone()

        if row is not None:
            # we have a cache!
            cache = row[0]
 #           logger.debug(cache)
            cache_datetime = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')

            logger.debug('cache_datetime is ')
            logger.debug(cache_datetime)
            logger.debug(datetime.datetime.utcnow())
            logger.debug((datetime.datetime.utcnow() - cache_datetime).total_seconds())
            logger.debug(config.CAСHE_LIVE_TIME)
            logger.debug((datetime.datetime.utcnow() - cache_datetime).total_seconds() > config.CAСHE_LIVE_TIME)

            if (datetime.datetime.utcnow() - cache_datetime).total_seconds() > config.CAСHE_LIVE_TIME:
                return None
            else:
                return cache
        else:
            return None
