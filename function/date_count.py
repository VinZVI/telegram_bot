import datetime
from calendar import monthrange
from datetime import  date


def deltatime(t1: str, t2: str):
    """ функция калькулятора дат
        принимает две даты в формте '%d.%m.%Y'
        возвращает время между датами в год месяц день (меяцев)"""
    t1 = datetime.datetime.strptime(t1, '%d.%m.%Y')
    t2 = datetime.datetime.strptime(t2, '%d.%m.%Y')
    dm = 0
    dy = 0
    lm = monthrange(t1.year, t1.month)
    if t2.day < t1.day:
        delta_d = lm[1] - t1.day + t2.day
        dm = 1
    else:
        delta_d = t2.day - t1.day

    if t2.month < t1.month:
        delta_m = 12 - t1.month + t2.month - dm
        dy = 1
    else:
        delta_m = t2.month - t1.month - dm

    delta_y = t2.year - t1.year - dy

    return f'{delta_y} г {delta_m} м {delta_d} д ({delta_y*12+delta_m} мес)'

# date_from = datetime.datetime.strptime(input('Введите дату с: '), '%d.%m.%Y')
# date_to = datetime.datetime.strptime(input('Введите дату по: '), '%d.%m.%Y')
# delta = deltatime(date_from, date_to)
# print (delta)

def cwt (d1: str, d2: str, np: int):
    """ функция считает чел/дни и чел/час
        принимает две даты "с,по" и количесво людей"""
    d1 = datetime.datetime.strptime(d1, '%d.%m.%Y')
    d2 = datetime.datetime.strptime(d2, '%d.%m.%Y')
    count = 0
    for d_ord in range(d1.toordinal(), d2.toordinal()):
        d = date.fromordinal(d_ord)
        if (d.weekday() >= 5):
            count += 1
    # print(count)
    delta = d2 - d1
    # print((delta.days - count)*np)
    plday = (delta.days - count) * np
    plhr = plday * 8
    return f'{plday} чел/дн\n{plhr} чел/час'

# date_from = datetime.datetime.strptime(input('Введите дату с: '), '%d.%m.%Y')
# date_to = datetime.datetime.strptime(input('Введите дату по: '), '%d.%m.%Y')
# #print(date_from, date_to)
# np = int(input('Введите количество людей: '))
# print (cwt(date_from, date_to, np))




