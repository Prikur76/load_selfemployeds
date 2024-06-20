#!/usr/bin/python
import logging
import re
import time
from datetime import datetime

import pandas as pd
import pytz
import requests
from googleapiclient.errors import HttpError

import settings as st
import spreadsheets as ss
from statusnpd_api import fetch_active_drivers, check_selfemployment_status

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        format='[%(levelname)s] - %(asctime)s - %(name)s - %(message)s',
        level=logging.INFO
    )
    try:
        login = st.ELEMENT_USER
        password = st.ELEMENT_PASSWORD
        active_drivers = fetch_active_drivers(login, password)

        inns = sorted(list(set(active_drivers['INN'].values)))
        inns = [i for i in inns if re.match('\d{11}', i)]
        check_date = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d')
        check_list = check_selfemployment_status(inns, check_date)
        checkout = pd.DataFrame(check_list)

        merged_roster = pd.merge(active_drivers, checkout, on='INN', how='left')
        merged_roster = merged_roster.fillna('')
        merged_roster['check_date'] = datetime.now(pytz.timezone('Europe/Moscow'))\
            .strftime('%d.%m.%Y %H:%M:%S')

        ss.batch_update_values(st.REPORT_ID, st.RANGE_FOR_SELFEMPLOYED,
                               merged_roster.values.tolist())

    except HttpError as ggl_http_err:
        logger.error(msg=f'Ошибка подключения гугла: {ggl_http_err}',
                     stack_info=False)
    except requests.exceptions.HTTPError as http_err:
        logger.error(msg=f'Ошибка http-запроса: {http_err}',
                     stack_info=False)
    except requests.exceptions.ChunkedEncodingError as chunked_err:
        logger.error(msg=f'Ошибка обработки пакета: {chunked_err}',
                     stack_info=False)
    except requests.exceptions.Timeout as timeout_err:
        logger.error(msg=f'Timeout: {timeout_err}', stack_info=False)
        time.sleep(300)
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(msg=f'Ошибка HTTP соединения: {conn_err}',
                     stack_info=False)
        time.sleep(60)


if __name__ == '__main__':
    main()
