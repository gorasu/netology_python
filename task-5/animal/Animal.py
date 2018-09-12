class Animal:
    __weight = 0
    __name = None

    def __init__(self, params):
        self.__weight = float(params['weight'])
        self.__name = params['name']

    @property
    def weight(self):
        return self.__weight

    @property
    def name(self):
        return self.__name

    def feed(self):
        print('Покормили')


class Animal_weight:
    """Класс для работы с весом животных"""
    animals = list()
    __heaviest_animal = None
    __full_weight = float(0)

    def __init__(self, animals: tuple):
        for animal in animals:
            self.__add(animal)

    def __set_heaviest_animal(self, animal: Animal):
        if not self.__heaviest_animal:
            self.__heaviest_animal = animal
        if self.__heaviest_animal.weight < animal.weight:
            self.__heaviest_animal = animal

    def __add(self, animal: Animal):
        self.__set_heaviest_animal(animal)
        self.__full_weight += float(animal.weight)
        self.animals.append(animal)

    @property
    def heaviest_animal(self):
        return self.__heaviest_animal

    @property
    def full_weight(self):
        return self.__full_weight


class Egg:
    """ Получить яйца с животного """
    __allowed = True

    def get_egg(self):

        if self.__allowed:
            print('Собрали яйца')
        else:
            print('Нет яиц')
        self.__allowed = False


class Vote:
    """ Голос животного """

    def vote(self):
        pass


class Milk:
    """ Доить молоко """
    __allowed = True

    def get_milk(self):
        if self.__allowed:
            print('Подоили молоко')
        else:
            print('Нет молока')
        self.__allowed = False


class Shearing:
    """ Стричь животное """
    __allowed = True

    def cut(self):
        if self.__allowed:
            print('Подстригли')
        else:
            print('Нет шерсти')
        self.__allowed = False


class Bird(Animal, Egg):
    """ Птицы """
    pass


class Goose(Bird, Vote):
    """ Гусь - несет яйца """

    def vote(self):
        return 'Га-га-га'


class Hen(Bird, Vote):
    """ Курица - несет яйца """

    def vote(self):
        return 'Ко-ко-ко'


class Cow(Animal, Vote, Milk):
    """ Корова - дает молоко """

    def vote(self):
        return 'Мууууу'


class Sheep(Animal, Vote, Shearing):
    """ Бараны - дают шерсть """

    def vote(self):
        return 'Беееее'


class Goat(Animal, Vote, Milk):
    """ Козы - дают молоко """

    def vote(self):
        return 'Меееее'


class Duck(Bird, Vote):
    """ Утка - несет яйца """

    def vote(self):
        return 'Кря-Кря'


class Turtle(Animal, Egg):
    """Черепаха - несет яйца"""
    pass
