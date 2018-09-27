from src.vk_api import *


class Command:

    def __init__(self):
        self.request = RequestApi(self.__get_token())
        currentUser = self.request.get('users.get', {})[0]
        self.currentUser = User.create(self.request, currentUser['id'])

    def __get_token(self):

        token = Token(6702992, ['user,friends'])
        print('Перейдите по ссылке для получения ключа {} '.format(token.get_auth_url()))
        return input('Введите полученный ключ:')

    def run(self):
        command = input('Введите команду (help, m, p):')
        command_list = ['help', 'm', 'p']
        if command not in command_list:
            print('Команда {} не зарегистрирована'.format(command))
        else:
            getattr(self, command)()

        self.run()

    def help(self):
        print('"m" - пересечение пользователей \n"p" - ссылка на профиль пользователя')

    def m(self):
        user_id = input('Введите user_id с которым нужно проверить пересечение:')
        user = User.create(self.request, user_id)
        users = self.currentUser & user
        if not users:
            print('Пересечений не найдено')
            return None

        for user in users:
            print('Общие друг {}, тип объекта {}'.format(user.user_id, type(user)))
        print('Всего:', len(users))

    def p(self):
        user_id = input('Введите user_id (по умолчанию текщий user):')
        if user_id:
            user = User.create(self.request, user_id)
        else:
            user = self.currentUser
        print(user.profile())


command = Command()
command.run()
