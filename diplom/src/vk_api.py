import time
import urllib.parse
from abc import ABC, abstractmethod

import requests


class VkApiError(Exception):
    """Исключение которое вызывается когда api вернуло ошибку"""

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
    """Исключение врмени запроса к API, срабатывает когда привышен лимит
    запросов в 1 секунду """
    pass


class VkApiErrorFactory:
    """Фабрика исключений занимается созданием исключений в зависимости от кода полученного от API"""

    def __init__(self, error: dict):
        self.__error = error

    def get_exception(self):
        if self.__error['error_code'] == 6:
            return VkApiTimeLimitError(self.__error['error_msg'], self.__error['error_code'])

        return VkApiError(self.__error['error_msg'], self.__error['error_code'])


class VkApiObserver(ABC):
    """Наблюдатель за статусом api"""

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

    def add_observer_wait(self, observer: VkApiObserver):
        """Регистрация наблюдателей за событием ожидания ответа от api"""
        self.__observers['wait'].append(observer)

    def add_observer_success(self, observer: VkApiObserver):
        """регитсрация налюдателей за успешным запросом к api"""
        self.__observers['success'].append(observer)

    def add_observer_error(self, observer: VkApiObserver):
        """регитсрация наблюдателей за ошибочными запросами к  api"""
        self.__observers['error'].append(observer)

    def _call_observers(self, state, status):
        """вызов наблюдателей на опраеделенном событии"""
        for observer in self.__observers.get(state):
            observer.update(status)

    def _main_params(self):
        """парметры которые всегда добавляются в запросу"""
        return {'access_token': self.__token, 'v': self.__version}

    def _call(self, method, params):
        """запрос к API"""
        params.update(self._main_params())
        request_url = urllib.parse.urljoin(self.__api_url, method)
        response = requests.get(request_url, params)
        result = response.json()
        if result.get('error'):
            raise VkApiErrorFactory(result['error']).get_exception()

        return result['response']

    def get(self, method, params: dict = {}):
        """клиенсткий метод для составления запросов к api
        занимается отправкой запроса и запуском событий для
        оповещения наблюдателей
        """
        try:
            result = self._call(method, params)
            self._call_observers('success', 'Api method {} success'.format(method))
            return result
        except VkApiTimeLimitError as e:
            self._call_observers('wait',  'Api method {} is wait'.format(method))
            time.sleep(0.35)
            return self.get(method, params)
        except VkApiError as e:
            self._call_observers('error', 'Error in api method {} code: {} message:{}'.format(method, e.code, e.message))
            raise e
