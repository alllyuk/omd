"""
Это небольшая история приключений утки одним осенним дождливым вечером.
Вы решаете судьбу утки и дальнейшее развитие событий
"""


def step1():
    print(
        'Утка-маляр 🦆 решила выпить зайти в бар. '
        'Взять ей зонтик? ☂️'
    )
    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input()

    if options[option]:
        return step2_umbrella()
    return step2_no_umbrella()


def step2_umbrella():
    print('Зонтик оказался взят не зря, ведь в баре случился дождь из пива, '
          'когда кто-то неаккуратно взболтал банку перед вскрытием :)')
    return


def step2_no_umbrella():
    print('Дождя не оказалось, так что зонтик действительно был не нужен :)'
          '\nЭто можно отметить баночкой пива в баре')
    return


if __name__ == '__main__':
    step1()
