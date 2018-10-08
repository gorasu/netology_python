from .vk_api import VkApi


class User:
    """Сущность для взамодействия с пользователем api"""
    def __init__(self, vk_api: VkApi, user_id):
        self.__user_id = user_id
        self.__vk_api = vk_api

    @property
    def user_id(self):
        return self.__user_id

    def get_groups(self):
        groups = self.__vk_api.get('groups.get', {'user_id': self.user_id, 'extended': 1})

        groups = list(map(lambda group: Group(self.__vk_api, group['id']), groups['items']))
        return groups

    def get_friend_ids(self):
        friend_ids = self.__vk_api.get('friends.get', {'user_id': self.user_id, 'extended': 1})
        return friend_ids['items']


class Group:
    """Сущность для взамодействия с группами api"""
    def __init__(self, vk_api: VkApi, group_id):
        self.__group_id = group_id
        self.__vk_api = vk_api

    @property
    def group_id(self):
        return self.__group_id

    def get_members_status(self, user_ids: list):
        return self.__vk_api.get('groups.isMember',
                                 {'group_id': self.group_id, 'user_ids': ','.join(str(uid) for uid in user_ids)})

    def get_group_info(self):
        group_info = self.__vk_api.get('groups.getById',
                                       {'group_id': self.group_id, 'fields': 'members_count'})

        return group_info[0]
