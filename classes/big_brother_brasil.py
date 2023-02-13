'''
Module BigBrotherBrasil
'''

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
        self.list_to_log = []


    def extract_and_transform_data(self) -> None:
        get_uol_page_data = requests.get(url=self.url, timeout=5)
        partial_result_div_regex = r'<div class=\"partial-result\">.*<\/div>'

        class_partial_result = re.findall(
            pattern=partial_result_div_regex,
            string=get_uol_page_data.text)[0]

        partial_result_regex = (
            '^<div class=\"partial-result\">\s<span class=\"perc-value\"\sng-b'
            'ind=\".+?\">([0-9]{1,}\,[0-9]{1,})%<\/span>.+?<span class=\"answe'
            'r-title\">(.+?)<\/span>.+?<div class=\"partial-result\">\s<span c'
            'lass=\"perc-value\"\sng-bind=\".+?\">([0-9]{1,}\,[0-9]{1,})%<\/sp'
            'an>.+?<span class=\"answer-title\">(.+?)<\/span>.+?<div class=\"p'
            'artial-result\">\s<span class=\"perc-value\"\sng-bind=\".+?\">([0'
            '-9]{1,}\,[0-9]{1,})%<\/span>.+?<span class=\"answer-title\">(.+?)'
            '<\/span>.+?<div class=\"partial-result\">\s<span class=\"perc-val'
            'ue\"\sng-bind=\".+?\">([0-9]{1,}\,[0-9]{1,})%<\/span>.+?<span cla'
            'ss=\"answer-title\">(.+?)<\/span>.+?Total\sde\s<span class=\"tota'
            'l-votes\"\sng-bind=\"totalVotes\">([0-9]{1,})<\/span>.+?$')

        partial_result = re.findall(
            pattern=partial_result_regex,
            string=class_partial_result)[0]

        housemate_partial_one = float(partial_result[0].replace(',', '.'))
        housemate_partial_two = float(partial_result[2].replace(',', '.'))
        housemate_partial_three = float(partial_result[4].replace(',', '.'))
        housemate_partial_four = float(partial_result[6].replace(',', '.'))
        total = int(partial_result[8])

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
                'amount': total * (housemate_partial_two / 100)
            },
            {
                'housemate': partial_result[5],
                'partial': housemate_partial_three,
                'amount': total * (housemate_partial_three / 100)
            },
            {
                'housemate': partial_result[7],
                'partial': housemate_partial_four,
                'amount': total * (housemate_partial_three / 100)
            }
        ]

        self.partial_result = sorted(
            self.partial_result,
            key=lambda d: d['partial'],
            reverse=True)

        self.list_to_log.append({
            'partial_result': self.partial_result,
            'poll_number': self.poll_number,
            'url': self.url,
            'datetime': self.datetime_and_poll_info
        })


    def create_tweet(self) -> None:
        msg = (
            'A @Splash_UOL está com as seguintes parciais para a Enquete do #B'
            'BB23 "Quem você quer eliminar no Paredão?"\n\n'
            f'1º {self.partial_result[0]["housemate"]}: '
            f'{self.partial_result[0]["partial"]}%\n'
            f'2º {self.partial_result[1]["housemate"]}: '
            f'{self.partial_result[1]["partial"]}%\n'
            f'3º {self.partial_result[2]["housemate"]}: '
            f'{self.partial_result[2]["partial"]}%\n'
            f'4º {self.partial_result[3]["housemate"]}: '
            f'{self.partial_result[3]["partial"]}%\n'
            f'\nTotal de Votos: {self.datetime_and_poll_info[0]["total"]}\n\n'
            f'{self.poll_number}º paredão do Big Brother Brasil 23\n'
            f'Atualizado em '
            f'{self.now["today"][2]}/{self.now["today"][1]}/'
            f'{self.now["today"][0]} às '
            f'{self.now["today"][3]}:{self.now["today"][4]}:'
            f'{self.now["today"][5]}')

        tweet = Twitter(msg=msg)
        self.list_to_log[0]['tweet'] = tweet.post()
