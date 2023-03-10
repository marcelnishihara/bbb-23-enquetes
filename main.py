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
        call_headers = Helpers.is_valid_call(headers_list=request.headers)

        if call_headers['is_valid_call']:
            print(f'Valid Call: {call_headers["is_valid_call"]}')

            sources = Sources(
                source_web_page=call_headers["Sourcewebpage"],
                poll=call_headers['Pollindex'],
                sources_json_file_path=call_headers['Sourcesjsonfile'])

            sources.compose_url()

            bbb = BigBrotherBrasil(
                url=sources.url,
                source_web_page=call_headers["Sourcewebpage"],
                poll_number=call_headers['Pollindex'],
                housemates_number=call_headers['Housematesnumber'])

            bbb.extract_and_transform_data()

            if call_headers['Tweet']:
                bbb.create_tweet(
                    housemates_number = call_headers['Housematesnumber'],
                    counter_limit = call_headers["Counterlimit"])

            return (json.dumps(obj=bbb.list_to_log), 200)

        else:
            msg = 'Unauthorized'
            print(f'{msg}: Invalid Call')
            return (msg, 401)

    except Exception:
        err = traceback.format_exc().replace('\n', ' ')
        print(f'Error: {err}')
        return ('Internal Server Error', 500)
