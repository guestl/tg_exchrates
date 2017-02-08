# -*- coding: utf-8 -*-

from tg_token import token
import config
import tg_exchrates_db_helper

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
