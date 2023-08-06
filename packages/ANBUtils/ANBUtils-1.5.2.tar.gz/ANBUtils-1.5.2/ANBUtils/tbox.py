# -*- coding:UTF-8 -*-
import time
from datetime import datetime, timedelta


def future(x):
    return (datetime.now() + timedelta(days=x)).strftime('%Y-%m-%d')


def utc2tz(dt, tz='E8'):
    if tz[0].upper() == 'E':
        h = int(tz[1:])
    elif tz[0].upper() == 'W':
        h = int(tz[1:]) * -1
    else:
        raise ValueError('[utc2tz] tz is KeyError!')

    return dt + timedelta(hours=h)


def today():
    return datetime.now().strftime("%Y-%m-%d")


def tomorrow():
    return future(1)


def yesterday():
    return future(-1)


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M')


def future_base(date, x):
    from datetime import datetime, timedelta
    base = datetime.strptime(date, "%Y-%m-%d")
    return (base + timedelta(days=x)).strftime('%Y-%m-%d')


def ts2str(x):
    if type(x) == str:
        x = int(x)
    return time.strftime("%Y-%m-%d", time.localtime(x))


def date_format(date, date_format='YYYY-MM-DD'):
    if len(date) == 10:
        if len(date.split('-')) == 3:
            date = date

        elif len(date.split('/')) == 3:
            date = date.replace('/', '-')

        elif len(date.split('_')) == 3:
            date = date.replace('_', '-')

    if len(date) == 6:
        y = date[:2]
        m = date[2:4]
        d = date[4:]
        if int(y) <= 30:
            y = '20' + y
        else:
            y = '19' + y
        date = '-'.join([y, m, d])

    if date_format == 'YYYY-MM-DD':
        return date
    elif date_format == 'YYMMDD':
        return date.replace('-', '')[2:]
    elif date_format == 'YYYY_MM_DD':
        return date.replace('-', '_')
