from loader_db_helper import db_loader_helper
from abc import ABCMeta, abstractmethod
import config
import random


class loader_default:

    __metaclass__ = ABCMeta

    # init db connection
    def __init__(self, loader_name):
        self.database = db_loader_helper()
        self.loader_name = loader_name
        self.daily_date = None

        self.user_agent = config.USER_AGENTS[random.randrange(len(config.USER_AGENTS))]
        self.headers = {'user-agent': self.user_agent}

    @abstractmethod
    # empty method
    def loadDailyData(self, dateForLoad):
        pass

    @abstractmethod
    # empty method
    def set_currency_list(self, currency_list):
        pass

    def get_rate_stc_type_string(self):
        """Get rate sources type for specific source

        Get type of rate source - cash rate or cards rate. We will compare these values with dict config.RATES_TYPES

        Returns:
            list -- list of IDX_TYPE fields from "global_variables" table
        """
        return self.database.get_rate_src_type_string(self.loader_name)

    def get_currency_list(self):
        return self.database.get_currency_list(self.loader_name)

    def get_domain(self):
        return self.database.get_domain(self.loader_name)

    def get_domains_history(self):
        return self.database.get_domains_history()

    # TODO: переделать. убрать scr_id, он же и так у нас уже есть
    def update_loader_log(self, src_id):
        self.database.update_loader_log(src_id)

    @abstractmethod
    # empy method
    def parseDailyData(self, dataForParse):
        pass

    # save parsed data into db
    def saveRatesData(self, parsedData):
        self.database.add_currency_rates_data(parsedData)

    # save cache data into db
    def saveCachedData(self, cached_data):
        if self.daily_date is not None:
            data_for_cache = [self.loader_name, self.daily_date, cached_data]
        else:
            raise ValueError("daily date is None")
        self.database.add_cache(data_for_cache)

    def check_cache(self, date_for_check):
        return self.database.check_and_load_cache(self.loader_name, date_for_check)
