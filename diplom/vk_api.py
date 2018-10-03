import urllib.parse
import requests


class VkApiError(Exception):

    def __init__(self, message, code):
        self.__code = code

    @property
    def code(self):
        return self.__code


class VkApi:

    __api_url = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.85'):
        self.__token = token
        self.__version = version

    def __main_params(self):
        return {'access_token': self.__token, 'v': self.__version}

    def get(self, method, params: dict = {}):
        params.update(self.__main_params())
        request_url = urllib.parse.urljoin(self.__api_url, method)
        response = requests.get(request_url, params)
        result = response.json()
        if result.get('error'):
            raise VkApiError(result['error']['error_msg'], result['error']['error_code'])
        return result['response']
