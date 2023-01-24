import os
import tweepy


class Twitter:
    def __init__(self, msg: str) -> None:
        self.msg = msg
        self.client = tweepy.Client(
            consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
            consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
            access_token=os.environ['TWITTER_ACCESS_TOKEN'],
            access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


    def post(self) -> dict:
        response = self.client.create_tweet(text=self.msg)
        return response.data
