import time

import pandas as pd
import requests


def fetch_active_drivers(login, password):
    '''
    Возвращает список работающих водителей 1с:Элемент
    '''
    url = 'https://taxi.0nalog.com:1711/Transavto/hs/Driver/v1/Get'
    auth = (login, password)
    payload = {
        'Status': 'Работает'
    }
    with requests.post(url=url, auth=auth,
                       json=payload, stream=True) as response:
        response.raise_for_status()
        drivers = response.json()
    roster = [
        profile for profile in drivers
        if profile['Car'] and  profile['ExternalCar'] == False
    ]
    active_drivers = pd.DataFrame(roster, columns=roster[0].keys())
    active_drivers = \
        active_drivers[['MetaId', 'DefaultID', 'ID', 'FIO', 'SNILS',
                        'INN','OGRN', 'KIS_ART_DriverId',
                        'CarDepartment']]\
            .fillna('')\
            .sort_values(by=['CarDepartment', 'FIO'], ascending=[True, True])
    return active_drivers


def check_selfemployment_status(inns: list, date: str) -> dict:
    '''
    Возвращает словарь с результатом проверки статуса самозанятости
    по списку ИНН на дату в формате YYYY-MM-DD
    '''
    url = 'https://statusnpd.nalog.ru:443/api/v1/tracker/taxpayer_status'
    check_result = []
    for inn in inns:
        payload = {
            'inn': inn,
            'requestDate': date
        }
        response = requests.post(url, json=payload, timeout=60)
        result = response.json()

        if response.status_code == 200:
            status, message = result.values()
            formatted_message = message.split(inn)[1]\
                .replace('плательщиком налога на профессиональный доход', 'СМЗ')\
                .strip()
            check_result.append(
                {
                    'INN': inn,
                    'check_status': status,
                    'message': formatted_message
                }
            )

        if response.status_code != 200:
            code, message = result.values()
            if 'Указан некорректный ИНН' in message:
                message = 'Некорректный ИНН'
            check_result.append(
                {
                    'INN': inn,
                    'check_status': False,
                    'message': message
                }
            )
        time.sleep(30)
    return check_result
