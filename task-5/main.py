from animal.Animal import *

animals_on_farm = [
    {'type': 'Goose'
        , 'init': {'name': 'Серый гусь', 'weight': 12}
     }

    , {'type': 'Goose'
        , 'init': {'name': 'Белый гусь', 'weight': 10}
       }

    , {'type': 'Hen'
        , 'init': {'name': 'Ко-Ко', 'weight': 1}
       }

    , {'type': 'Hen'
        , 'init': {'name': 'Кукареку', 'weight': 12}
       }

    , {'type': 'Cow'
        , 'init': {'name': 'Манька', 'weight': 150}
       }

    , {'type': 'Sheep'
        , 'init': {'name': 'Барашек', 'weight': 40}
       }

    , {'type': 'Sheep'
        , 'init': {'name': 'Кудрявый', 'weight': 50}
       }

    , {'type': 'Goat'
        , 'init': {'name': 'Рога', 'weight': 50}
       }

    , {'type': 'Goat'
        , 'init': {'name': 'Копыта', 'weight': 45}
       }

    , {'type': 'Duck'
        , 'init': {'name': 'Кряква', 'weight': 5}
       }

    , {'type': 'Turtle'
        , 'init': {'name': 'Леонардо', 'weight': 0.9}
       }
]

animals = list()
for animal_on_farm in animals_on_farm:
    _class = globals()[animal_on_farm['type']]
    animal = _class(animal_on_farm['init'])
    animals.append(animal)

animal_weight = AnimalWeight(animals)

for animal in animals:
    print(type(animal), animal.name)
    animal.feed()
    if isinstance(animal, Egg):
        animal.get_egg()
    if isinstance(animal, Vote):
        print(animal.vote())
    if isinstance(animal, Milk):
        animal.get_milk()
    if isinstance(animal, Shearing):
        animal.cut()

    print()

print('Самый тяжелый:', animal_weight.heaviest_animal.name, '', animal_weight.heaviest_animal.weight)
print('Общий вес:', animal_weight.full_weight)

# Домашнее задание к лекции 1.5 «Классы и их применение в Python»

# Вы приехали помогать на ферму Дядюшки Джо и видите вокруг себя множество разных животных:
# * гусей "Серый" и "Белый"
# * корову "Маньку"
# * овец "Барашек" и "Кудрявый"
# * кур "Ко-Ко" и "Кукареку"
# * коз "Рога" и "Копыта"
# * и утку "Кряква"

# Со всеми животными вам необходимо как-то взаимодействовать:
# * кормить
# * корову и коз доить
# * овец стричь
# * собирать яйца у кур, утки и гусей
# * различать по голосам(коровы мычат, утки крякают и т.д.)

# ## Задача №1
# Нужно реализовать классы животных, не забывая использовать наследование,
# определить *общие методы* взаимодействия с животными и
# дополнить их в дочерних классах, если потребуется.

# ## Задача №2
# Для каждого животного из списка должен существовать экземпляр класса.
# Каждое животное требуется накормить и подоить/постричь/собрать яйца, если надо.

# ## Задача №3
# У каждого животного должно быть определено имя(self.name) и вес(self.weight). 
# - Необходимо посчитать общий вес всех животных(экземпляров класса);
# - Вывести название самого тяжелого животного.

# ## Задача №4
# Для подготовки к следующей лекции прочитайте про [
# работу с файлами](https://pythonworld.ru/tipy-dannyx-v-python/fajly-rabota-s-fajlami.html).
