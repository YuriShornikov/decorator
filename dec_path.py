import os
import datetime


def logger(path):


    def __logger(old_function):
        arg_list = []
        kwarg_dict = {}
        result_list = []

        def new_function(*args, **kwargs):
            with open(path, 'w+', encoding='utf-8') as file:
                result = old_function(*args, **kwargs)
                time_func = str(datetime.datetime.now())
                file.write(f'{time_func} \n')
                file.write(f'{old_function.__name__} \n')
                arg_list.append(args)
                kwarg_dict.update(kwargs)
                for value in kwargs.values():
                    arg_list.append(value)
                file.write(f'{arg_list} {kwarg_dict} \n')
                result_list.append(str(result))
                file.write(f'{result_list} \n')
                return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()