import json
import time
from pprint import pprint
from src import User, Group

from vk_api import VkApi, VkApiObserver


class ObserverSuccess(VkApiObserver):

    def update(self):
        print('.', sep=' ', end=' ', flush=True)


class ObserverWait(VkApiObserver):

    def update(self):
        print('w', sep=' ', end=' ', flush=True)


def group_to_json(group: Group):
    info = group.get_group_info()
    return {'name': info['name'], 'gid': info['id'], 'members_count': info['members_count']}


vk = VkApi('ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae')
vk.add_observer_success(ObserverSuccess())
vk.add_observer_wait(ObserverWait())

user = User(vk, '171691064')
groups = user.get_groups()
friend_ids = user.get_friend_ids()

group_with_out_friends = []
for group in groups:

    group_member = group.get_members_status(friend_ids)
    mebmers = list(filter(lambda member: member['member'] == 1, group_member))

    if not mebmers:
        group_with_out_friends.append(group)

with open('groups.json', 'w') as file:
    json.dump(group_with_out_friends, file, indent=4, default=group_to_json)

