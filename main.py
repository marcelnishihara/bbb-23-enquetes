from Classes.BigBrotherBrasil import BigBrotherBrasil
from Classes.Helpers import Helpers


def main(request):
    try:
        call_headers = {}

        for header in request.headers:
            call_headers[header[0]] = header[1]

        is_valid_call = Helpers.is_google_apps_script_project_call(call_headers)

        if is_valid_call:
            print(f'Valid Call: {is_valid_call}')

            url_base = 'https://www.uol.com.br/splash/bbb/enquetes'

            url_voting = [
                {
                    'date': '/2023/01/23',
                    'html': '/enquete-uol-qual-dupla-deve-ir-paro-o-quarto-secreto-do-bbb-23-vote.htm'
                }
            ]

            index = 0
            url = f'{url_base}{url_voting[index]["date"]}{url_voting[index]["html"]}'

            bbb = BigBrotherBrasil(
                url=url,
                poll_number=index + 1)

            bbb.extract_and_transform_data()
            response = bbb.create_tweet()
            return (response, 200)

        else:
            print(f'Unauthorized: Invalid Call')
            return ('Unauthorized', 401)

    except Exception as err:
        print(f'Error: {err}')
        return ('Internal Server Error', 500)
