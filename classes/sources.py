'''
'''

import json
import os
import requests


class Sources:

    def __init__(
        self,
        source_web_page: str,
        poll: int,
        sources_json_file_path: str
        ) -> None:
        self.__source_web_page = source_web_page
        self.__poll = poll
        self.__sources_json_file_path = sources_json_file_path

        self.__sources = { 'splash': 0, 'splash_filler': 1 }
        self.__sources_json_file_content = []

        self.url = ''


    def __get_sources_json_file(self) -> None:
        sources_json_file_url = (
            f'{os.environ["SOURCES_JSON_FILE_URL_BASE"]}'
            f'{self.__sources_json_file_path}')

        response = requests.get(
            url=sources_json_file_url,
            timeout=10)

        self.__sources_json_file_content = json.loads(s=response.text)


    def compose_url(self) -> None:
        self.__get_sources_json_file()

        if self.__source_web_page in self.__sources:
            json_file_content = self.__sources_json_file_content
            index = self.__sources[self.__source_web_page]

            self.url += (
                f'{json_file_content[index]["url_base"]}'
                f'{json_file_content[index]["polls"][self.__poll]["date"]}'
                f'{json_file_content[index]["polls"][self.__poll]["html"]}')
