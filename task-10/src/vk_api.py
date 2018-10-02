import urllib.parse
import requests


class RequestApiError(Exception):
    pass


class Token:

    def __init__(self, app_id: int, scope: list):
        self.__app_id = app_id
        self.__scope = scope

    def get_auth_url(self):
        auth_data = {
            'client_id': self.__app_id
            , 'display': 'page'
            , 'scope': ','.join(self.__scope)
            , 'response_type': 'token'
        }

        return '?'.join(('https://oauth.vk.com/authorize', urllib.parse.urlencode(auth_data)))


class RequestApi:

    def __init__(self, token, version='5.85'):
        self.__token = token
        self.__version = version

    def __main_params(self):
        return {'access_token': self.__token, 'v': self.__version}

    def __api_url(self):
        return 'https://api.vk.com/method/'

    def get(self, method, params: dict) -> requests:
        params.update(self.__main_params())
        request_url = urllib.parse.urljoin(self.__api_url(), method)
        response = requests.get(request_url, params)
        result = response.json()
        if result.get('error'):
            raise RequestApiError(result['error']['error_msg'])
        return result['response']


class User:

    def __init__(self, request: RequestApi, user_id):
        self.__user_id = user_id
        self.__request = request

    def profile(self):
        return 'https://vk.com/id{}'.format(self.user_id)

    @property
    def user_id(self):
        return self.__user_id

    def friends_mutual(self, target_uid):

        friend_ids = self.__request.get('friends.getMutual',
                                        {'source_uid': self.user_id
                                            , 'target_uid': target_uid})
        return list(map(lambda friend_id: __class__(self.__request, friend_id), friend_ids))

    def __and__(self, user):
        return self.friends_mutual(user.user_id)

    def __str__(self):
        return self.profile()

