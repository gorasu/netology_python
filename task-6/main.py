def clean_string(string):
    return string.strip()


def recipe_format(recipe_list):

    result = dict()
    recipe_name = recipe_list.pop(0)
    recipe_ingridient_count = recipe_list.pop(0)
    result[recipe_name] = list()
    ingredient_list = list()
    for ingredient in recipe_list:
        ingredient = ingredient.split('|')
        ingredient = [i.strip() for i in ingredient]
        ingredient_list.append({'ingredient_name': ingredient[0], 'quantity': ingredient[1], 'measure': ingredient[2]})

    result[recipe_name] = ingredient_list
    return result


def get_shop_list_by_dishes(dishes, person_count):
    recipes = get_recipes()
    ingredients = dict()
    for dish in dishes:
        for ingredient in recipes[dish]:
            ingredients[ingredient['ingredient_name']] = {'quantity': int(ingredient['quantity']), 'measure': ingredient['measure']}
    for ingredient in ingredients.values():
        ingredient['quantity'] *= int(person_count)
    return ingredients


def get_recipes():
    with open('cook_book.txt') as cook_book_file:
        recipes = dict()
        recipe = list()
        line_list = cook_book_file.readlines()
        line_iteration_count = (len(line_list) - 1)
        for index, line in enumerate(line_list):
            line = clean_string(line)
            if line and (index != line_iteration_count):
                recipe.append(line)
            else:
                if recipe:
                    recipes.update(recipe_format(recipe))
                recipe = list()
    return recipes


shop_list = get_shop_list_by_dishes(['Омлет', 'Фахитос'], 40)
print(shop_list)
