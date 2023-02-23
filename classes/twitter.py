'''
'''
import os
import tweepy


class Twitter:
    def __init__(self, data: list) -> None:
        self.msg = ''
        self.data = data[0]
        self.client = tweepy.Client(
            consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
            consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
            access_token=os.environ['TWITTER_ACCESS_TOKEN'],
            access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


    def compose_msg(self) -> None:
        self.msg = (
            'A @Splash_UOL está com as seguintes parciais para a Enquete do #B'
            'BB23 "Quem você quer eliminar no Paredão?"\n\n')

        for index, housemate in enumerate(self.data['partial_result']):
            housemate_partial = str(housemate["partial"]).replace('.', ',')

            self.msg += (
                f'{index + 1}º {housemate["housemate"]}: '
                f'{housemate_partial}%\n')

        print(f'\n\n\n{self.data}\n\n\n')
        now = self.data['now']['today']

        self.msg += (
            f'\nTotal de Votos: {self.data["total"]}\n\n'
            f'{self.data["poll_number"]}º paredão do Big Brother Brasil 23'
            '\nAtualizado em '
            f'{now[2]}/{now[1]}/{now[0]} às {now[3]}:{now[4]}:{now[5]}')


    def post(self) -> dict:
        response = self.client.create_tweet(text=self.msg)
        return response.data
