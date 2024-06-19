import re
import textwrap as tw
from datetime import datetime


def remove_chars(s):
    return re.sub(r'[^0-9a-zA-Zа-яА-Яё]+', ' ', s)


def format_date_string(date_string, format='%d.%m.%Y'):
    """Форматирует строку с датой в формат даты"""
    old_format = datetime.strptime(
        date_string, '%Y-%m-%dT%H:%M:%S')
    new_format = old_format.strftime(format)
    return new_format


def check_phone(phone):
    """Возвращает True or False как результат проверки соответствия
    маске мобильного телефона
    """
    result = re.match(
        r"^(\+7|7|8)?[\s\-]?\(?9[0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$",
        phone.strip()
    )
    return bool(result)


# Группа функций для обработки данных водителей
def clean_phone(row_data):
    """Возвращает строку с телефонами водителя или False"""
    clean_data = re.sub(r'[^0-9]+', ' ', row_data)
    clean_phone = ', '.join(
        re.findall(r'([\+7|8|7]+[0-9]{10})', clean_data)
    )
    if not clean_phone:
        return None, False
    return clean_phone, True


def format_fullname(row_data):
    """Возвращает строку с ФИО водителя"""
    fullname = '%s %s' % (row_data['last_name'].strip(), row_data['first_name'].strip())
    if str(row_data['middle_name']).strip():
        fullname +=  f" {row_data['middle_name']}"
    return fullname
