import urllib.parse
import requests


class RequestApiError(Exception):
    pass


class RequestApi:

    def __init__(self, token, version='5.85'):
        self.__token = token
        self.__version = version

    def __main_params(self):
        return {'access_token': self.__token, 'v': self.__version}

    def __api_url(self):
        return 'https://api.vk.com/method/'

    def request(self, method, params: dict) -> requests:
        params.update(self.__main_params())
        request_url = urllib.parse.urljoin(self.__api_url(), method)
        response = requests.get(request_url, params)
        result = response.json()
        if result.get('error'):
            raise RequestApiError(result['error']['error_msg'])
        return result
