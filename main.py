from Classes.BigBrotherBrasil import BigBrotherBrasil
from Classes.Helpers import Helpers
from sources.sources import Sources

import traceback


def main(request):
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
            print(f'Unauthorized: Invalid Call')
            return ('Unauthorized', 401)

    except Exception:
        err = traceback.format_exc().replace('\n', ' ')
        print(f'Error: {err}')
        return ('Internal Server Error', 500)
