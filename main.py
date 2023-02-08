'''
Module Docstring
'''


import json
import traceback

from classes.big_brother_brasil import BigBrotherBrasil
from classes.helpers import Helpers
from classes.sources import Sources


def main(request):
    '''
    Function Docstring
    '''
    try:
        call_headers = {}

        for header in request.headers:
            key = header[0]
            value = header[1]

            if key == 'Tweet':
                call_headers[key] = bool(int(value))
            elif key == 'Pollindex':
                call_headers[key] = int(value)
            else:
                call_headers[key] = value

        is_valid_call = Helpers.is_google_apps_script_project_call(call_headers)

        if is_valid_call:
            print(f'Valid Call: {is_valid_call}')

            sources = Sources(index=call_headers['Pollindex'])
            sources.compose_splash_uol_url()

            bbb = BigBrotherBrasil(
                url=sources.url,
                poll_number=call_headers['Pollindex'])

            bbb.extract_and_transform_data()

            if call_headers['Tweet']:
                bbb.create_tweet()

            return (json.dumps(obj=bbb.list_to_log), 200)

        else:
            msg = 'Unauthorized'
            print(f'{msg}: Invalid Call')
            return (msg, 401)

    except Exception:
        err = traceback.format_exc().replace('\n', ' ')
        print(f'Error: {err}')
        return ('Internal Server Error', 500)
