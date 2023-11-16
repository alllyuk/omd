import click
from random import randint
from typing import Callable

PIZZA_TYPES = ['Margherita', 'Pepperoni', 'Hawaiian']
PIZZA_EMOJI = {'Margherita': '', 'Pepperoni': '', 'Hawaiian': ''}


class Margherita:
    def __init__(self, size: str = 'L'):
        self.size = size
        self.recipe = {
            'tomato_sauce': 100,
            'mozzarella': 400,
            'tomatoes': 200
        }

    def dict(self, only_names: bool = False) -> dict:
        if only_names:
            print(', '.join(self.recipe.keys()))
        else:
            print(self.recipe)


class Pepperoni:
    def __init__(self, size: str = 'L'):
        self.size = size
        self.recipe = {
            'tomato_sauce': 100,
            'mozzarella': 350,
            'pepperoni': 250
        }

    def dict(self, only_names: bool = False) -> dict:
        if only_names:
            print(', '.join(self.recipe.keys()))
        else:
            print(self.recipe)


class Hawaiian:
    def __init__(self, size: str = 'L'):
        self.size = size
        self.recipe = {
            'tomato_sauce': 100,
            'mozzarella': 350,
            'chicken': 150,
            'pineapples': 150
        }

    def dict(self, only_names: bool = False) -> dict:
        if only_names:
            print(', '.join(self.recipe.keys()))
        else:
            print(self.recipe)


def log(template: str) -> str:
    def decorator(f: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            print(template.format(randint(1, 60)))
            return f(*args, **kwargs)
        return wrapper
    return decorator


@log('Приготовили за {}с!')
def func_cooking(pizza):
    """
    Готовит пиццу
    :param pizza:
    :return:
    """
    pass


@log('Доставили за {}с!')
def func_delivery(pizza):
    """
    Доставляет пиццу
    :param pizza:
    :return:
    """
    pass


@log(' Забрали за {}с!')
def func_pickup(pizza):
    """
    Самовывоз
    :param pizza:
    :return:
    """
    pass


@click.group()
def cli():
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: str, delivery: bool):
    """
    Готовит и доставляет пиццу
    :param pizza:
    :param delivery:
    :return:
    """
    if pizza.lower().capitalize() not in PIZZA_TYPES:
        print('Такой пиццы не существует.')
        print('Выберите одну из следующих пицц: {}.'.format(
            ', '.join(PIZZA_TYPES)
            ))
        return

    func_cooking(pizza)
    if delivery:
        func_delivery(pizza)
    else:
        func_pickup(pizza)


@cli.command()
def menu():
    """
    Выводит меню
    :return:
    """
    for pizza_type in PIZZA_TYPES:
        class_ = globals()[pizza_type]

        print(f'{pizza_type} {PIZZA_EMOJI[pizza_type]}: ', end='')
        class_().dict(only_names=True)


if __name__ == '__main__':
    cli()
