import csv


def start() -> None:
    """
    Prints the greeting and available options
    :return: None
    """
    print('Добро пожаловать! Выберите, что вам требуется:')
    print('1. Показать иерархию команд.')
    print('2. Показать сводный отчет по департаментам.')
    print('3. Сохранить в csv-формате сводный отчет по департаментам.')
    print('Введите номер пункта в поле ниже:')


def show_hierarchy(filename: str) -> dict:
    """
    Calculates and show team hierarchy in every department
    :param filename: name of csv file containing the data
    :return: hierarchy dictionary like {department : teams, }
    """
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)

        departments: dict = {}
        for row in reader:
            department = row[1]
            team = row[2]
            if department not in departments.keys():
                departments[department] = [team]
            elif team not in departments.get(department):
                departments[department].append(team)

    print("{:20} {:50}".format('Департамент', 'Команды'))
    print()
    for dep, teams in departments.items():
        print("{:20} {:50}".format(dep, ', '.join(teams)))

    return departments


def make_stats(filename: str) -> dict:
    """
    Calculates statistics for each department
    :param filename: name of csv file containing the data
    :return: statistics dictionary like {department : {statistics}, }
    """
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)

        stats: dict = {}
        for row in reader:
            department = row[1]
            salary = int(row[5])
            if department not in stats.keys():
                stats[department] = {'count': 1,
                                     'min_salary': salary,
                                     'max_salary': salary,
                                     'sum_salary': salary}
            else:
                stats[department]['count'] += 1
                stats[department]['sum_salary'] += salary
                if stats[department]['min_salary'] > salary:
                    stats[department]['min_salary'] = salary
                elif stats[department]['max_salary'] < salary:
                    stats[department]['max_salary'] = salary
    return stats


def show_stats(stats: dict) -> None:
    """
    Prints the department stats from make_stats function
    :param stats: ready statistics dictionary like {department : {statistics},}
    :return: None
    """
    print("{:>12} {:^15} {:^10} {:^10} {:^10}".format('Департамент',
                                                      'Численность',
                                                      'Мин. ЗП',
                                                      'Макс. ЗП',
                                                      'Сред. ЗП'))
    print()
    for dep, stat in stats.items():
        print("{:>12}{:^15} {:^10} {:^10} {:^10.0f}".format(dep,
                                                            stat['count'],
                                                            stat['min_salary'],
                                                            stat['max_salary'],
                                                            stat['sum_salary'] / stat['count']))
    return


def save_stats(stats: dict, report_name: str) -> None:
    """
    Saves the department stats from make_stats function to csv-file
    :param stats: ready statistics dictionary like {department : {statistics},}
    :param report_name: name to save csv-file with statistics
    :return: None
    """
    print(f'Сводный отчет по департаментам будет сохранен как {report_name}')

    with open(report_name, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Департамент',
                         'Численность',
                         'Мин. ЗП',
                         'Макс. ЗП',
                         'Сред. ЗП'])
        for dep, stat in stats.items():
            row = [dep,
                   stat['count'],
                   stat['min_salary'],
                   stat['max_salary'],
                   round(stat['sum_salary'] / stat['count'])
                   ]
            writer.writerow(row)
    return


if __name__ == '__main__':

    csv_name = 'Corp_Summary.csv'
    report_csv_name = 'Departments.csv'

    start()
    while True:
        n = input()
        if n == '1':
            show_hierarchy(csv_name)
            break

        elif n == '2':
            ready_stats = make_stats(csv_name)
            show_stats(ready_stats)
            break

        elif n == '3':
            ready_stats = make_stats(csv_name)
            save_stats(ready_stats, report_csv_name)
            break

        else:
            print('Введите число от 1 до 3 и повторите попытку')
