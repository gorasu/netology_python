import time
import urllib.parse
from abc import ABC, abstractmethod

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


class VkApiObserver(ABC):

    @abstractmethod
    def update(self):
        pass


class VkApi:
    __api_url = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.85'):
        self.__token = token
        self.__version = version
        self.__observers = {'wait': [], 'success': [] }

    def add_observer_wait(self, observer: VkApiObserver):
        self.__observers['wait'].append(observer)

    def add_observer_success(self, observer: VkApiObserver):
        self.__observers['success'].append(observer)

    def _call_observers(self, state):
        for observer in self.__observers.get(state):
            observer.update()

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
            result = self._call(method, params)
            self._call_observers('success')
            return result
        except VkApiTimeLimitError as e:
            self._call_observers('wait')
            time.sleep(1)
            return self.get(method, params)
