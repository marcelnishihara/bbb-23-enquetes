'''
'''

import json

from classes.helpers import Helpers


class Sources:
    def __init__(
        self,
        index: int,
        source: str = 'splash',
        path: str = './sources/sources.json'
        ) -> None:
        self.url = ''
        self.source = source
        self.index = index

        sources_file_read = Helpers.read_file(path=path)
        print(f'File reading response: {sources_file_read}')
        self.sources = sources_file_read['data']


    def compose_splash_uol_url(self) -> None:
        indexes = {
            'splash': 0
        }

        if self.source == 'splash':
            self.url = (
                f'{self.sources[indexes["splash"]]["url_base"]}'
                f'{self.sources[indexes["splash"]]["polls"][self.index]["date"]}'
                f'{self.sources[indexes["splash"]]["polls"][self.index]["html"]}')

        print(self.url)
