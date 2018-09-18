from typing import List
import json
import xml.etree.ElementTree as ET


class News:
    __description = None

    def __init__(self, news):
        self.__description = news['description']

    @property
    def description(self):
        return self.__description


class Parser:
    __news = list()
    __file = None

    def __init__(self, file):
        self.__news = list()
        self.__file = file

    def file(self):
        return self.__file

    def _add_news(self, news: News):
        self.__news.append(news)

    def get_news(self) -> List[News]:
        return self.__news

    def parse(self):
        pass


class ParserXml(Parser):

    def parse(self):

        tree = ET.parse(self.file())
        news_tags = tree.findall('channel/item')
        for news in news_tags:
            description = news.find('description').text
            self._add_news(News({'description': description}))


class ParserJson(Parser):

    def parse(self):
        with(open(self.file())) as json_file:
            json_str = json.load(json_file)
        for news in json_str['rss']['channel']['items']:
            self._add_news(News(news))


class ParserTxt(Parser):

    def parse(self):
        with(open(self.file())) as txt_file:
            txt_news = txt_file.read()
            news_list = txt_news.split("\n")
        for description in news_list:
            self._add_news(News({'description':description}))


class ParserBuilder:
    __file = None

    def __init__(self, file):
        self.__file = file

    def __is_json(self):
        return self.__file.find('.json') is not -1

    def __is_xml(self):
        return self.__file.find('.xml') is not -1

    def __is_txt(self):
        return self.__file.find('.txt') is not -1

    def build(self) -> Parser:
        if self.__is_json():
            return ParserJson(self.__file)
        if self.__is_xml():
            return ParserXml(self.__file)
        if self.__is_txt():
            return ParserTxt(self.__file)
        print('для файла', self.__file, 'нет парсера')


class TopNewsWord:
    __news = None

    def __init__(self, news: List[News]):
        self.__news = news

    def __words_len(self, string: str) -> dict:
        words = string.split(" ")
        words = list(filter(lambda w: len(w.strip()), words))
        words_len = list(map(lambda w: len(w), words))
        return dict(zip(words, words_len))

    def by_letter_count(self, max_word_len, max_word_count=10):
        words = dict()
        result = list()
        for news in self.__news:
            words.update(self.__words_len(news.description))
        for word, word_len in words.items():
            if word_len >= max_word_len:
                result.append(word)
        result.sort(key=len, reverse=True)
        return result[:max_word_count]
