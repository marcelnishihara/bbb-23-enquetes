'''
'''

import json
import os

from datetime import datetime
from pytz import timezone


class Helpers:

    @staticmethod
    def get_datetime() -> None:
        date = datetime.now(tz=timezone(zone='Brazil/East'))

        today = [
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second
        ]

        for index, value in enumerate(today):
            today[index] = f'0{value}' if value < 10 else value

        datetime_formatted = (
            f'{today[0]}_{today[1]}_{today[2]}_'
            f'{today[3]}h{today[4]}min{today[5]}s')

        return {
            'datetime': datetime_formatted,
            'today': today
        }


    @staticmethod
    def read_file(
        path,
        enconding: str = 'utf-8',
        is_json: bool = True,
        ) -> dict:
        '''
        static method open_file()
        '''
        file_opened = open(
            file=path,
            mode='r',
            encoding=enconding)

        read_data = file_opened.read()
        data = json.loads(s=read_data) if is_json else read_data
        return { 'success': True, 'path': path, 'data': data }


    @staticmethod
    def create_headers_dict(headers_list: list) -> dict:
        headers_dict = {}

        for header in headers_list:
            key = header[0]
            value = header[1]

            if key == 'Tweet':
                headers_dict[key] = bool(int(value))
            elif key == 'Pollindex' or key == 'Housematesnumber':
                headers_dict[key] = int(value)
            else:
                headers_dict[key] = value

        return headers_dict


    @staticmethod
    def is_valid_call(headers_list: list) -> dict:
        headers = Helpers.create_headers_dict(headers_list=headers_list)
        headers['is_valid_call'] = False

        project_uuid = os.environ['PROJECT_UUID']
        is_uuid_valid = headers['Projectuuid'] == project_uuid
        headers['is_valid_call'] = True if is_uuid_valid else False

        headers['Projectuuid'] = (
            f'{headers["Projectuuid"][0:4]}***{headers["Projectuuid"][-4:]}')

        print(f'Call Headers: {json.dumps(headers)}')
        return headers
