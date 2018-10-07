import time
import urllib.parse
from abc import ABC, abstractmethod

import requests


class VkApiError(Exception):

    def __init__(self, message, code):
        self.__code = code
        self.__message = message

    @property
    def code(self):
        return self.__code

    @property
    def message(self):
        return self.__message


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
    def update(self, status):
        pass


class VkApi:
    """VkApi взаимодействет с api вконтакте
    в объект можно добавить наблюдателей за состоянием запросов api
    add_observer_wait - наблюдатели за событием паузы по запросам
    add_observer_success - наблюдатели за успешным запросом к api
    add_observer_error - наблюдатель для регтисрации ошибок приложения
    """
    __api_url = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.85'):
        self.__token = token
        self.__version = version
        self.__observers = {'wait': [], 'success': [], 'error': []}
        self.__status = None

    def add_observer_wait(self, observer: VkApiObserver):
        self.__observers['wait'].append(observer)

    def add_observer_success(self, observer: VkApiObserver):
        self.__observers['success'].append(observer)

    def add_observer_error(self, observer: VkApiObserver):
        self.__observers['error'].append(observer)

    def _call_observers(self, state):
        for observer in self.__observers.get(state):
            observer.update(self.__status)

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
        self.__status = None
        try:
            result = self._call(method, params)
            self.__status = 'Method {} success'.format(method)
            self._call_observers('success')
            return result
        except VkApiTimeLimitError as e:
            self.__status = 'Method {} is wait'.format(method)
            self._call_observers('wait')
            time.sleep(0.35)
            return self.get(method, params)
        except VkApiError as e:
            self.__status = 'Error in method {} code: {} message:{}'.format(method, e.code, e.message)
            self._call_observers('error')
            raise e
