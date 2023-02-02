'''
Module BigBrotherBrasil
'''

import json
import re
import requests

from classes.helpers import Helpers
from classes.twitter import Twitter


class BigBrotherBrasil:
    '''
    Class BigBrotherBrasil
    '''
    def __init__(self, url: str, poll_number: int) -> None:
        self.datetime_and_poll_info = []
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
            '^<div class=\"partial-result\">\s<span class=\"perc-value\"\sng'
            '-bind=\".+?\">([0-9]{1,}\,[0-9]{1,})%<\/span>.+?<span class=\"a'
            'nswer-title\">(.+?)<\/span>.+?<div class=\"partial-result\">\s<'
            'span class=\"perc-value\"\sng-bind=\".+?\">([0-9]{1,}\,[0-9]{1,'
            '})%<\/span>.+?<span class=\"answer-title\">(.+?)<\/span>.+?<div'
            ' class=\"partial-result\">\s<span class=\"perc-value\"\sng-bind'
            '=\".+?\">([0-9]{1,}\,[0-9]{1,})%<\/span>.+?<span class=\"answer'
            '-title\">(.+?)<\/span>.+?Total\sde\s<span class="total-votes"\s'
            'ng-bind="totalVotes">([0-9]{1,})<\/span>\svotos.+?$')

        partial_result = re.findall(
            pattern=partialResultRegex,
            string=class_partial_result)[0]

        housemate_partial_one = float(partial_result[0].replace(',', '.'))
        housemate_partial_two = float(partial_result[2].replace(',', '.'))
        housemate_partial_three = float(partial_result[4].replace(',', '.'))
        total = int(partial_result[6])

        self.datetime_and_poll_info.append({
                'datetime': self.now['datetime'],
                'total': total,
                'poll_number': self.poll_number
        })

        self.partial_result = [
            {
                'housemate': partial_result[1],
                'partial': housemate_partial_one,
                'amount': total * (housemate_partial_one / 100)
            },
            {
                'housemate': partial_result[3],
                'partial': housemate_partial_two,
                'amount': total * (housemate_partial_one / 100)
            },
            {
                'housemate': partial_result[5],
                'partial': housemate_partial_three,
                'amount': total * (housemate_partial_two / 100)
            }
        ]


    def create_tweet(self) -> None:
        print(f'\n\n{self.partial_result}\n\n')
        msg = (
            f'A @Splash_UOL está com as seguintes parciais para a Enquete do #BBB23 '
            '"Quem você quer eliminar no Paredão?"\n\n'
            f'{self.partial_result[0]["housemate"]}: {self.partial_result[0]["partial"]}%\n'
            f'{self.partial_result[1]["housemate"]}: {self.partial_result[1]["partial"]}%\n'
            f'{self.partial_result[2]["housemate"]}: {self.partial_result[2]["partial"]}%\n'
            f'Total de Votos: {self.datetime_and_poll_info[0]["total"]}\n\n'
            f'{self.poll_number}º paredão do Big Brother Brasil 23\n'
            f'Atualizado em '
            f'{self.now["today"][2]}/{self.now["today"][1]}/{self.now["today"][0]} às '
            f'{self.now["today"][3]}:{self.now["today"][4]}:{self.now["today"][5]}')

        tweet = Twitter(msg=msg)
        response = tweet.post()

        partial_result_sorted = sorted(
            self.partial_result,
            key=lambda d: d['partial'],
            reverse=True)

        list_to_log = [
            {
                'partial_result': partial_result_sorted,
                'poll_number': self.poll_number,
                'url': self.url,
                'datetime': self.datetime_and_poll_info,
                'response': response
            }
        ]

        string_to_return = json.dumps(list_to_log)
        print(string_to_return)
        return string_to_return