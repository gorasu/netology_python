import os

import requests
from urllib.parse import urlencode

API_KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


class YandexApiError(Exception):
    pass


class YandexTranslate:
    __api_url_format = 'https://translate.yandex.net/api/v1.5/tr.json/translate?{}'

    def __init__(self, api_key):
        self.__api_key = api_key
        self.__format = 'plain'
        self.__lang = 'ru-en'

    def _url(self):
        params = {'key': self.__api_key, 'lang': self.__lang, 'format': self.__format}
        return self.__api_url_format.format(urlencode(params))

    def set_format(self, value):
        self.__format = value

    def set_lang(self, from_lang, to_lang):
        self.__lang = '{}-{}'.format(from_lang, to_lang)

    def traslate(self, text):
        params = {
            'text': text
        }

        response = requests.post(self._url(), params=params)
        response = response.json()
        if response['code'] != 200:
            raise YandexApiError(response['message'])
        return ''.join(response['text'])


class YandexApiBuilder:
    def __init__(self, api_key):
        self.__api_key = api_key

    def build(self):
        return YandexTranslate(self.__api_key)


def is_txt_extension(file):
    return os.path.splitext(file)[1].lower() == '.txt'


def translate_it(source_file, result_file, from_lang, to_lang='ru'):
    if not os.path.exists(source_file):
        raise FileExistsError('Файл {} с текстом для перевода не существует '.format(source_file))

    result_dir = os.path.dirname(result_file)
    if not os.path.exists(result_dir):
        raise NotADirectoryError('Директории {} для файла результата не существет'.format(result_dir))

    with open(source_file) as file:
        source_text = file.read()

    translate_builder = YandexApiBuilder(
        'trnsl.1.1.20180924T143709Z.6825569223ac94fd.5fa82d7238defa3e8f024b77c3e57b09a4c37cba')
    translate = translate_builder.build()
    translate.set_lang(from_lang, to_lang)
    result_text = translate.traslate(source_text)

    with open(result_file, 'w+') as file:
        file.write(result_text)


source_dir = os.path.join('.', 'file')
for file in os.listdir(source_dir):
    file_path = os.path.join(source_dir, file)
    if not (os.path.isfile(file_path) and is_txt_extension(file_path)):
        continue

    lang_from = os.path.splitext(file)[0]
    translate_it(file_path, os.path.join('.', 'result', '{}-{}.txt'.format(lang_from, 'RU')), lang_from.lower())
