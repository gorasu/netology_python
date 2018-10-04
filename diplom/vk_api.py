import time
import urllib.parse
import requests


class VkApiError(Exception):

    def __init__(self, message, code):
        self.__code = code

    @property
    def code(self):
        return self.__code


class VkApiTimeLimitError(VkApiError):
    pass


class VkApiErrorFactory:

    def __init__(self, error: dict):
        self.__error = error

    def get_exception(self):
        if self.__error['error_code'] == 6:
            return VkApiTimeLimitError(self.__error['error_msg'], self.__error['error_code'])

        return VkApiError(self.__error['error_msg'], self.__error['error_code'])


class VkApi:
    __api_url = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.85'):
        self.__token = token
        self.__version = version

    def __main_params(self):
        return {'access_token': self.__token, 'v': self.__version}

    def _call(self, method, params):
        params.update(self.__main_params())
        request_url = urllib.parse.urljoin(self.__api_url, method)
        response = requests.get(request_url, params)
        result = response.json()
        if result.get('error'):
            raise VkApiErrorFactory(result['error']).get_exception()

        return result['response']

    def get(self, method, params: dict = {}):
        try:
            return self._call(method, params)
        except VkApiTimeLimitError as e:
            time.sleep(1)
            return self.get(method, params)
