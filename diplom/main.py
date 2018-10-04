import json
import time
from pprint import pprint

from vk_api import *

access_token = input('Введите token:')

vk = VkApi(access_token)
user_id = vk.get('users.get')
user_id = user_id[0]['id']
groups = vk.get('groups.get', {'user_id': user_id, 'extended': 1})

group_with_out_friends = []
for group in groups['items']:

    gropu_info = vk.get('groups.getMembers', {'group_id': group['id'], 'filter': 'friends'})
    if not gropu_info['count']:
        group_with_out_friends.append(group)
    print('ID группы {}'.format(group['id']), gropu_info)

with open('groups.json', 'w') as file:
    json.dump(group_with_out_friends, file, indent=4, ensure_ascii=False)

pprint(group_with_out_friends)
