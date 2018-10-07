import datetime
import json
from src import User, Group, VkApi, VkApiObserver


class ObserverSuccess(VkApiObserver):

    def update(self, status):
        print('.', sep=' ', end=' ', flush=True)


class ObserverWait(VkApiObserver):

    def update(self, status):
        print('w', sep=' ', end=' ', flush=True)


class ObserverError(VkApiObserver):

    def update(self, status):
        print('e', sep=' ', end=' ', flush=True)


class ObserverLog(VkApiObserver):

    def __init__(self):
        self.__statuses = []

    def update(self, status):
        self.__statuses.append('time:{} status: {}'.format(datetime.datetime.now(), status))
        with open('vk_api.log', 'w') as file:
            file.write('{}\n'.format(self.__statuses))


def group_to_json(group: Group):
    info = group.get_group_info()
    return {'name': info['name'], 'gid': info['id'], 'members_count': info['members_count']}


def get_groups_without_friends(groups, friend_ids):
    group_with_out_friends = []
    for group in groups:

        group_member = group.get_members_status(friend_ids)
        group_members = list(filter(lambda member: member['member'] == 1, group_member))

        if not group_members:
            group_with_out_friends.append(group)
    return group_with_out_friends


vk = VkApi('ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae')
vk.add_observer_success(ObserverSuccess())
vk.add_observer_wait(ObserverWait())
vk.add_observer_error(ObserverError())
vk.add_observer_error(ObserverLog())
user_id = input('Введите ID пользователя (171691064):') or 171691064

user = User(vk, user_id)
groups = user.get_groups()
friend_ids = user.get_friend_ids()
group_with_out_friends = get_groups_without_friends(groups, friend_ids)

with open('groups.json', 'w') as file:
    json.dump(group_with_out_friends, file, indent=4, default=group_to_json)
