'''
Module Docstring
'''

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
            call_headers[header[0]] = header[1]

        is_valid_call = Helpers.is_google_apps_script_project_call(call_headers)

        if is_valid_call:
            print(f'Valid Call: {is_valid_call}')

            index = 2
            sources = Sources(index=index)
            sources.compose_splash_uol_url()

            bbb = BigBrotherBrasil(
                url=sources.url,
                poll_number=index)

            bbb.extract_and_transform_data()
            response = bbb.create_tweet()
            return (response, 200)

        else:
            msg = 'Unauthorized'
            print(f'{msg}: Invalid Call')
            return (msg, 401)

    except Exception:
        err = traceback.format_exc().replace('\n', ' ')
        print(f'Error: {err}')
        return ('Internal Server Error', 500)
