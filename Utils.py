import scrapy
from dirbot.items import Website, News
import dirbot.settings
import datetime
import logging
import dateutil.parser
import traceback
import re
import time

def parseDT(strDT):
    ret = None
    try:
        # replace nian yue ri in Chinese
        dtCreated = re.sub('[^\d:]+', ' ', strDT)   # replace non digit and colon
        # parse
        dtCreated = dateutil.parser.parse(dtCreated)
    except:
        strToLog = 'empty dtCreated: %s'%strDT
        logging.log(logging.ERROR, strToLog)

    if ret is None:
        ret = 'NULL'

    return ret

