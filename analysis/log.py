import os
import datetime


def generate_log(log, fail=False):
    name_log = os.getenv('FILE_LOG', 'log.txt')
    path_log = os.getenv('PATH_LOG', os.getcwd())

    file_log = os.path.join(path_log, name_log)

    with open(file_log, 'a') as file:
        print(log.lower())
        file.writelines('{}: {}\n'.format(datetime.datetime.now(), log.replace('\n', ' -- ').lower()))
