import click
from random import randint
from typing import Callable

PIZZA_TYPES = ['Margherita', 'Pepperoni', 'Hawaiian']
PIZZA_EMOJI = {
    'Margherita': '\U0001F9C0',
    'Pepperoni': '\U0001F355',
    'Hawaiian': '\U0001F34D'
    }


class Margherita:
    """ Margherita pizza class with recipe """
    def __init__(self, size: str = 'L', status='Not exists'):
        """
        Initialize class
        :param size: pizza size, default is 'L'
        :param status: pizza ready status
        """
        self.size = size
        self.recipe = {
            'tomato_sauce': 100,
            'mozzarella': 400,
            'tomatoes': 200
        }
        self.status = status

    def dict(self, print_only_names: bool = False):
        """
        Print pizza ingredients
        :param print_only_names: whether to print only names of ingredients
        :return:
        """
        if print_only_names:
            print(', '.join(self.recipe.keys()))
        else:
            print(self.recipe)


class Pepperoni:
    """ Pepperoni pizza class with recipe """
    def __init__(self, size: str = 'L', status='Not exists'):
        """
        Initialize class
        :param size: pizza size, default is 'L'
        :param status: pizza ready status
        """
        self.size = size
        self.recipe = {
            'tomato_sauce': 100,
            'mozzarella': 350,
            'pepperoni': 250
        }
        self.status = status

    def dict(self, print_only_names: bool = False):
        """
        Print pizza ingredients
        :param print_only_names: whether to print only names of ingredients
        :return:
        """
        if print_only_names:
            print(', '.join(self.recipe.keys()))
        else:
            print(self.recipe)


class Hawaiian:
    """ Hawaiian pizza class with recipe """
    def __init__(self, size: str = 'L', status='Not exists'):
        """
        Initialize class
        :param size: pizza size, default is 'L'
        :param status: pizza ready status
        """
        self.size = size
        self.recipe = {
            'tomato_sauce': 100,
            'mozzarella': 350,
            'chicken': 150,
            'pineapples': 150
        }
        self.status = status

    def dict(self, print_only_names: bool = False):
        """
        Print pizza ingredients
        :param print_only_names: whether to print only names of ingredients
        :return:
        """
        if print_only_names:
            print(', '.join(self.recipe.keys()))
        else:
            print(self.recipe)


def log(template: str) -> Callable:
    """
    Decorator to print time on the specified template
    :param template:
    :return: function decorator
    """
    def decorator(f: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            print(template.format(randint(1, 60)))
            return f(*args, **kwargs)
        return wrapper
    return decorator


@log('\U0001F468\U0000200D\U0001F373 Приготовили за {}с!')
def func_cooking(pizza_type: str, size: str):
    """
    Bakes the pizza
    :param pizza_type: Margherita or Pepperoni or Hawaiian
    :param size: pizza size from L to XL
    :return: baked_pizza instance
    """
    baked_pizza = globals()[pizza_type.lower().capitalize()]
    baked_pizza.size = size
    baked_pizza.status = 'Baked'
    return baked_pizza


@log('\U0001F698 Доставили за {}с!')
def func_delivery(baked_pizza):
    """
    Delivers the pizza
    :param baked_pizza: baked_pizza instance
    :return: baked_pizza instance with "delivered" status
    """
    baked_pizza.status = 'Delivered'
    return baked_pizza


@log('\U0001F3EC Забрали за {}с!')
def func_pickup(baked_pizza):
    """
    Picks up the pizza
    :param baked_pizza: baked_pizza: baked_pizza instance
    :return: baked_pizza instance with "picked up" status
    """
    baked_pizza.status = 'Picked up'
    return baked_pizza


@click.group()
def cli():
    """ Need for decorator click.group """
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza_type', nargs=1)
@click.argument('size', default='L', nargs=1)
def order(pizza_type: str, size: str, delivery: bool):
    """
    Serves an order of pizza from preparation to the customer.
    :param pizza_type: Margherita or Pepperoni or Hawaiian
    :param size: pizza size from L to XL
    :param delivery: delivery required if True, else pick up by customer
    :return:
    """
    if pizza_type.lower().capitalize() not in PIZZA_TYPES:
        print('Такой пиццы не существует.')
        print('Выберите одну из следующих пицц: {}.'.format(
            ', '.join(PIZZA_TYPES)
            ))
        return

    if size not in ['L', 'XL']:
        print('Такого размера пиццы нет. Выберите размер L или XL.')
        return

    baked_pizza = func_cooking(pizza_type, size)
    if delivery:
        func_delivery(baked_pizza)
    else:
        func_pickup(baked_pizza)


@cli.command()
def menu():
    """
    Show available menu to customer
    :return:
    """
    for pizza_type in PIZZA_TYPES:
        class_ = globals()[pizza_type]

        print(f'{pizza_type} {PIZZA_EMOJI[pizza_type]}: ', end='')
        class_().dict(print_only_names=True)
    return


if __name__ == '__main__':
    cli()

    assert Margherita().dict() == {
            'tomato_sauce': 100,
            'mozzarella': 400,
            'tomatoes': 200
        }

    assert Pepperoni().dict() == {
            'tomato_sauce': 100,
            'mozzarella': 350,
            'pepperoni': 250
        }

    assert Hawaiian().dict() == {
            'tomato_sauce': 100,
            'mozzarella': 350,
            'chicken': 150,
            'pineapples': 150
        }

    assert order('Hawaiian', 'XS')() == \
        'Такого размера пиццы нет. Выберите размер L или XL.'

    assert order('Pesto', 'L')() == \
        'Такой пиццы не существует.' \
        '\nВыберите одну из следующих пицц: Margherita, Pepperoni, Hawaiian'
