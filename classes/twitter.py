'''
'''

import os
import tweepy


class Twitter:
    '''Class Twitter
    '''

    def __init__(self, data: list) -> None:
        self.msg = ''
        self.data = data[0]
        self.__client = tweepy.Client(
            consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
            consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
            access_token=os.environ['TWITTER_ACCESS_TOKEN'],
            access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


    def __compose_msg(self, counter_limit: int) -> None:
        '''Method __compose_msg
        '''
        self.msg = (
            'A @Splash_UOL está com as seguintes parciais para a Enquete do #B'
            f'BB23 "{self.data["question"]}"\n\n')

        counter = 0
        three_firsts_sum = 0

        while counter < counter_limit:
            housemate = self.data['partial_result'][counter]
            housemate_partial = str(housemate["partial"]).replace('.', ',')
            three_firsts_sum += housemate["partial"]

            self.msg += (
                f'{counter + 1}º {housemate["housemate"]}: '
                f'{housemate_partial}%\n')

            counter += 1

        if self.data['source_web_page'] == 'splash_filler':
            other_housemates = format((100 - three_firsts_sum), '.2f')
            other_housemates = str(other_housemates).replace('.', ',')
            self.msg += f'Os demais somam {other_housemates}%\n'

        self.msg += f'\nTotal de Votos: {self.data["total"]}\n'

        if self.data['source_web_page'] == 'splash':
            self.msg += (
                f'{self.data["poll_number"]}º paredão do '
                'Big Brother Brasil 23\n')

        now = self.data['now']['today']

        self.msg += ('\n🕒 '
            f'{now[2]}/{now[1]}/{now[0]} às {now[3]}:{now[4]}:{now[5]}')


    def post(self, counter_limit: int) -> dict:
        '''Method post
        '''
        self.__compose_msg(counter_limit=counter_limit)
        response = self.__client.create_tweet(text=self.msg)
        return response.data
