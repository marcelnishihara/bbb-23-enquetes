'''
'''

import json


class Sources:
    def __init__(
        self, 
        index: int,
        source: str = 'splash'
        ) -> None:
        self.url = ''
        self.source = source
        self.index = index

        sources_json_file = open(
            file='./sources/sources.json',
            mode='r',
            encoding='utf-8')
        
        self.sources = json.loads(s=sources_json_file.read())
        sources_json_file.close()


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
