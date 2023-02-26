import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            with open(path, 'w+', encoding='utf-8') as f:
                result = old_function(*args, **kwargs)
                print(result)
                json.dump(result, f, indent=5)
                return result

        return new_function

    return __logger

HOST = 'https://spb.hh.ru/search/vacancy?text=python+Django+Flask&salary=&area=1&area=2&ored_clusters=true&enable_snippets=true'

data_list = []
data_USD = []

#т.к. объявления на нескольких страницах, организовываем цикл
for i in range(0, 4):
    url = HOST + '&page=' + str(i)

    def get_headers():
        headers = Headers(browser='firefox', os='win')
        return headers.generate()

    hh = requests.get(url, headers=get_headers())
    hh_python = hh.text

    soup = BeautifulSoup(hh_python, features='lxml')
    hh = soup.find_all('div', class_='serp-item')

    for prof in hh:
        #вывод ссылки на объявление
        href_code = prof.find('a')
        href = href_code['href']
        #вывод зарплаты
        salary_code = prof.find('span', class_='bloko-header-section-3')
        if salary_code == None:
            salary = ' '
        else:
            salary = salary_code.text

        #вывод наименование компании
        name_code = prof.find('div', class_='vacancy-serp-item__meta-info-company')
        name = name_code.text
        #вывод города
        city_code = prof.find('div', attrs= {'data-qa': 'vacancy-serp__vacancy-address'}, class_='bloko-text')
        city = city_code.text.split(',')#отделяем город от остального ненужного

        #форма для всех вакансий
        form_all = {
            'href': href,
            'salary': salary.replace('\u202f', ' '),
            'company': name.replace('\xa0', ' '),
            'city': city[0]
        }
        data_list.append(form_all)

#
#         #форма для USD вакансий
        form_USD = {
            'href': href,
            'salary': salary.replace('\u202f', ' '),
            'company': name.replace('\xa0', ' '),
            'city': city[0]
        }
        #проверка в какой валюте предлагают оплату
        salary_USD = salary.split(' ')
        if salary_USD[-1] == 'USD':
            data_USD.append(form_USD)#добавление словарей в список USD


#Добавил 2 функции для декоратора на запись файлов
@logger('hh.json')
def all():
    return data_list
all()

@logger('hh_USD.json')
def USD():
    return data_USD
USD()

#было до декоратора

# with open('hh.json', 'w', encoding='utf-8') as f:
#     json.dump(data_list, f, indent=5)
#
# with open('hh_USD.json', 'w', encoding='utf-8') as f:
#     json.dump(data_USD, f, indent=5)