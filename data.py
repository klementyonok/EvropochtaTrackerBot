import json
import re

import requests

from sql import read_track_num, create_track, read_track_row_count

URL = 'https://evropochta.by/api/track.json'

headers = requests.utils.default_headers()

headers.update(
    {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 '
                      'Safari/537.36 OPR/40.0.2308.81',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate, lzma, sdch',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    }
)


def track_validation(track_number: str) -> bool:
    """ Проверяет на соответствие шаблону BY123456789012 """
    if re.match('[B][Y]\d{12}', track_number) is not None:
        return True


def response_from_evropochtaby(track_number: str) -> json:
    """ Делает запрос к серверу """
    try:
        response = requests.get(
            URL,
            params={'number': track_number},
            headers=headers)
    except Exception as err:
        print("Ошибка: " + str(err))
    else:
        return response


def check_for_error(data: dict) -> bool:
    """ Проверяет на наличие ошибки """
    if 'Error' in data['data'][0]:
        return True
    return False


def error_number(data: dict) -> str:
    """ Определяет номер ошибки """
    error = data['data'][0]['Error']
    return error


def error_description(error_num: str) -> str:
    """ Определяет описание ошибки """
    error_dict = {
        '0': 'Неправильный трек 😵‍💫 Трек должен соответствовать шаблону BY123456789012',
        '33': 'Информация об отправлении не найдена 🤷‍♂',
    }
    return error_dict.get(error_num)


def formatting_track_information(data: dict, row_count_in_database: int):
    """ Сохраняет дату и статус трека """
    text = ''
    row_count_in_response = len(data['data'])
    if row_count_in_response > row_count_in_database:
        text = '❗Новый статус трека❗\n'
    for i in range(row_count_in_response):
        date = data['data'][i]['Timex']
        status = data['data'][i]['InfoTrack']
        text += f"{date} {status}\n"
    return text


def track_information_output(track_number: str, user_id: int, description: str) -> str:
    """ Выводит информацию о треке """
    if track_validation(track_number):
        response = response_from_evropochtaby(track_number)
        data = response.json()
        if check_for_error(data):
            error_num = error_number(data)
            return error_description(error_num)
        else:
            if read_track_num(track_number, user_id) != track_number:
                row_count = len(data['data'])
                create_track(track_number, user_id, row_count, description)
            row_count_in_database = read_track_row_count(track_number, user_id)
            return formatting_track_information(data, row_count_in_database)

    else:
        return error_description('0')
