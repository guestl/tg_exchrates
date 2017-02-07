# -*- coding: utf-8 -*-

# helper for work with database
import config
#import loader_db_helper
from loader_def_class import loader_default

import io
from lxml import etree
from datetime import datetime
import requests

import logging

logger = logging.getLogger(__name__)
logger.setLevel(config.LOGGER_LEVEL)


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
#        logger.info("load Daily Data for date")
#        logger.info(dateForLoad.date())
        self.daily_date = dateForLoad.date()
        str_date_for_load = self.daily_date.strftime('%d.%m.%Y')

        # temporary get data from a file
        loadedData = ''

        # check for cache for bai.kz
        cachedData = self.check_cache(self.daily_date)

        if cachedData is None:
            logger.debug("There is no cache")
            try:
                req = requests.post(self.url, data={'data': str_date_for_load}, headers=self.headers)
                loadedData = req.text

                self.update_loader_log(self.loader_name)
            except Exception as e:
                logger.error("Error during loading process")
                logger.error(e)
                loadedData = None
        else:
            logger.debug("We have a cache")
            loadedData = cachedData

        if loadedData and cachedData is None:
            self.saveCachedData(loadedData)
        elif loadedData is None:
            return None
        return loadedData

    def parseDailyData(self, dataForParse):
        """Parse downloaded data
        Arguments:
            dataForParse {string} -- [String with data for parsing]

        Returns:
            [list] -- [return list of specific data (source, avrg_value, rate_datetime, curidfrom, curidto, quant) or 'None']
        """
        # setup default values
        quant = 1
        avrg_value = 0
        rate_type_for_source = self.get_rate_stc_type_string()
        currencies_list = self.get_currency_list()
        # logger.debug(currencies_list)

        return_list = []

#        currency_dict = {}

        parser = etree.HTMLParser()
        tree = etree.parse(io.StringIO(dataForParse), parser)

        counter = tree.xpath('count(//table[@class="cv_table"]/tbody/tr)')
        try:
            counter = int(counter)
        except Exception as e:
            logger.error(e)
            return None

        logger.debug(counter)
        for elem in range(1, counter + 1):
            rows = tree.xpath('//table[@class="cv_table"]/tbody/tr[' + str(elem) + ']')

            for row in rows:
                rate_type = row.xpath('.//td/span/strong')
                if len(rate_type) > 0:
                    rate_type_s = rate_type[0].text
                    logger.debug(rate_type_s)
                    logger.debug(rate_type_for_source)

                if rate_type_s == config.RATES_TYPES[rate_type_for_source]:
                    cur_row_list = tree.xpath('//table[@class="cv_table"]/tbody//tr[ ' + str(elem) + ']/th/text()')
                    # logger.debug("cur_row_list is:")
                    # logger.debug(cur_row_list)
                    # logger.debug("elem is:")
                    # logger.debug(elem)

                    if len(cur_row_list) > 0:
                        cur_row = ''.join(cur_row_list[0].split())
                        # logger.debug("cur_row is:")
                        # logger.debug(cur_row)
                        # logger.debug("currencies_list is:")
                        # logger.debug(currencies_list)

                        if cur_row in currencies_list:
                            # logger.debug("cur_row")
                            # logger.debug(cur_row)
                            currency_id = cur_row
                            tds = row.xpath('.//td[text()]')
                            if len(tds) == 5:  # 5 elements in entire row
                                try:
                                    quant = int(tds[0].text)
                                    buy_value = float(tds[2].text)
                                    sell_value = float(tds[3].text)
                                    rate_datetime = datetime.strptime(tds[4].text, "%d.%m.%Y")

                                    return_list.append([self.loader_name, buy_value, sell_value, avrg_value,
                                                        rate_datetime, config.CUR_KZT, currency_id, quant])

                                    # logger.debug(return_list)

                                except Exception as e:
                                    logger.error(e)
                                    return None
                            else:
                                logger.error("Found nothing while parsing")
                                return None
        if return_list is not None:
            logger.debug("return_list after parsing is:")
            logger.debug(return_list)
            return return_list
        return None
