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

    def __init__(self,
        url: str,
        poll_number: int,
        housemates_number: int = 3) -> None:
        self.url = url
        self.poll_number = poll_number
        self.housemates_number = housemates_number
        self.now = Helpers.get_datetime()
        self.partial_result = []
        self.list_to_log = []


    def extract_and_transform_data(self) -> None:
        get_uol_page_data = requests.get(url=self.url, timeout=5)

        regexp = self.__compose_regexp(
            housemates_number=self.housemates_number)

        class_partial_result = re.findall(
            pattern=regexp['data']['partial_result_div'],
            string=get_uol_page_data.text)[0]

        partial_result = re.findall(
            pattern=regexp['data']['partial_result_regexp'],
            string=class_partial_result)[0]

        housemate_info_data_pairs = int((len(partial_result) - 1) / 2)
        total = int(partial_result[-1])

        for index in range(housemate_info_data_pairs):
            housemate_index = index * 2

            housemate_partial = float(partial_result[housemate_index] \
                .replace(',', '.'))

            self.partial_result.append({
                'housemate': partial_result[housemate_index + 1],
                'partial': housemate_partial,
                'amount': total * (housemate_partial / 100)})

        self.partial_result = sorted(
            self.partial_result,
            key=lambda d: d['partial'],
            reverse=True)

        self.list_to_log.append({
            'partial_result': self.partial_result,
            'url': self.url,
            'now': self.now,
            'total': total,
            'poll_number': self.poll_number})


    def create_tweet(self) -> None:
        tweet = Twitter(data=self.list_to_log)
        tweet.compose_msg()
        self.list_to_log[0]['tweet'] = tweet.post()


    @staticmethod
    def __compose_regexp(housemates_number: int = 3) -> dict:
        '''
        Static method compose_regexp
        '''
        sources_file_read = Helpers.read_file(path='./sources/regexp.json')
        partial_result_regex = ''

        for _ in range(housemates_number):
            partial_result_regex += (
                f'{sources_file_read["data"]["housemate_data"]}.+?')

        sources_file_read['data']['partial_result_regexp'] = (
            '^'
            f'{partial_result_regex}'
            f'{sources_file_read["data"]["total"]}'
            '$')

        return sources_file_read
