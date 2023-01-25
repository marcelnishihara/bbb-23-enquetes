from Classes.Helpers import Helpers
from Classes.Twitter import Twitter

import json
import re
import requests


class BigBrotherBrasil:
    def __init__(self, url: str, poll_number: int) -> None:
        self.url = url
        self.poll_number = poll_number
        self.now = Helpers.get_datetime()
        self.partial_result = []


    def extract_and_transform_data(self) -> None:
        get_uol_page_data = requests.get(self.url)
        partial_result_div_regex = r'<div class=\"partial-result\">.*<\/div>'

        class_partial_result = re.findall(
            pattern=partial_result_div_regex,
            string=get_uol_page_data.text)[0]

        partialResultRegex = (
            '^<div class="partial-result">\s<span class="perc-value"\sng-bind=\".+?">'
            '([0-9]{2,}\,[0-9]{1,})%<\/span>.+?<span class="answer-title">(.+?)<\/spa'
            'n>.+<div class="partial-result">\s<span class="perc-value"\sng-bind=\".+'
            '?">([0-9]{2,}\,[0-9]{1,})%<\/span>.+?<span class="answer-title">(.+?)<\/'
            'span>.+?Total\sde\s<span class="total-votes"\sng-bind="totalVotes">([0-9'
            ']{1,})<\/span>\svotos.+?$')

        partial_result = re.findall(
            pattern=partialResultRegex,
            string=class_partial_result)[0]

        housemate_partial_one = float(partial_result[0].replace(',', '.'))
        housemate_partial_two = float(partial_result[2].replace(',', '.'))
        total = int(partial_result[4])

        self.partial_result = [
            { 
                'datetime': self.now['datetime'],
                'total': total,
                'poll_number': self.poll_number
            },
            {
                'housemate': partial_result[1],
                'partial': housemate_partial_one,
                'amount': total * (housemate_partial_one / 100)
            },
            {
                'housemate': partial_result[3],
                'partial': housemate_partial_two,
                'amount': total * (housemate_partial_two / 100)
            }
        ]


    def create_tweet(self) -> None:
        msg = (
            f'A @Splash_UOL está com as seguintes parciais para a Enquete do #BBB23 '
            '"Quem você quer eliminar no Paredão?"\n\n'
            f'{self.partial_result[1]["housemate"]}: {self.partial_result[1]["partial"]}%\n'
            f'{self.partial_result[2]["housemate"]}: {self.partial_result[2]["partial"]}%\n'
            f'Total de Votos: {self.partial_result[0]["total"]}\n\n'
            f'{self.poll_number}º paredão do Big Brother Brasil 23\n'
            f'Atualizado em '
            f'{self.now["today"][2]}/{self.now["today"][1]}/{self.now["today"][0]} às '
            f'{self.now["today"][3]}:{self.now["today"][4]}:{self.now["today"][5]}')

        tweet = Twitter(msg=msg)
        response = tweet.post()

        list_to_log = [
            { 
                'partial_result': self.partial_result,
                'poll_number': self.poll_number,
                'url': self.url,
                'now': self.now['datetime'],
                'response': response
            }
        ]

        string_to_return = json.dumps(list_to_log)
        print(string_to_return)
        return string_to_return
