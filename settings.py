from environs import Env

env = Env()
env.read_env()

ELEMENT_USER = env.str('ELEMENT_USER')
ELEMENT_PASSWORD = env.str('ELEMENT_PASSWORD')

REPORT_ID = env.str('REPORT_SPREADSHEETS_ID')
RANGE_FOR_SELFEMPLOYED = env.str('RANGE_FOR_SELFEMPLOYED')
PARKS = [
    {
        'city': 'МОСКВА',
        'id': env.str('MSK_PARK_ID'),
        'api_key': env.str('MSK_X_API_KEY')
    },
    {
        'city': 'МОСКВА (СОЦИАЛЬНЫЙ)',
        'id': env.str('SPECIAL_PARK_ID'),
        'api_key': env.str('SPECIAL_X_API_KEY')
    },
    {
        'city': 'МОСКВА',
        'id': env.str('ELS_PARK_ID'),
        'api_key': env.str('ELS_X_API_KEY')
    },
    {
        'city': 'Екатеринбург',
        'id': env.str('EKB_PARK_ID'),
        'api_key': env.str('EKB_X_API_KEY')
    },
    {
        'city': 'Ярославль',
        'id': env.str('YAR_PARK_ID'),
        'api_key': env.str('YAR_X_API_KEY')
    },
    {
        'city': 'ЧЕЛЯБИНСК',
        'id': env.str('CHL_PARK_ID'),
        'api_key': env.str('CHL_X_API_KEY')
    }
]
