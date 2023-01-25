from datetime import datetime
from pytz import timezone

import json
import os


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
    def log(
        string_to_log: str, 
        filename: str,
        prefix: str = 'log',
        extension: str = 'json',
        ) -> None:
        file = (
            f'{prefix}_'
            f'{filename}.'
            f'{extension}')

        f = open(file=file, mode='w', encoding='utf-8')
        f.write(string_to_log)
        f.close()


    @staticmethod
    def is_google_apps_script_project_call(headers: dict) -> bool:
        is_valid_call = False
        project_uuid = os.environ['PROJECT_UUID']
        is_uuid_valid = headers['Projectuuid'] == project_uuid
        is_valid_call = True if is_uuid_valid else False
        
        headers['Projectuuid'] = (
            f'{headers["Projectuuid"][0:4]}'
            '***'
            f'{headers["Projectuuid"][-4:]}')

        print(f'Call Headers: {json.dumps(headers)}')
        return is_valid_call
