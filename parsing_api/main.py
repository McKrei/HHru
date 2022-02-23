import requests
import sqlite3
import datetime as dt
from fake_useragent import UserAgent

import use_selenium

'''
Парсим ID Вакансий пытаясь обойти ограничение в 2000 вакансий на один запрос.
закидываем в таблицу
CREATE TABLE all_vacancy_id(id INTEGER);
'''


HEADERS         = {'user-agent': UserAgent().random}
URL             = 'https://api.hh.ru/vacancies'
db              = sqlite3.connect('VacanciesDB.db')
cursor          = db.cursor()
count_vac_write = 0

def new_headers():
    global HEADERS
    HEADERS = {'user-agent': UserAgent().random}

# Получаем лист с ID специальностей
def get_specialization_list():
    link           = 'https://api.hh.ru/specializations'
    reception      = requests.get(url=link, headers=HEADERS)
    result_list    = []
    reception_json = reception.json()

    for el in reception_json:
        for id in el['specializations']:
            result_list.append(id['id'])
    
    return result_list

# Получаем лист с ID индустрий
def get_industries_list():
    link           = 'https://api.hh.ru/industries'
    result_list    = []
    reception      = requests.get(url=link, headers=HEADERS)
    reception_json = reception.json()

    for industries in reception_json:
        result_list.append(industries['id'])

    return result_list


# Запись в БД
def write_vacancies_db(list_tupls):
    try:
        cursor.executemany('INSERT INTO all_vacancy_id VALUES(?);', list_tupls)
        db.commit()
    except Exception as er:
        db.commit()
        print(f'Ошибка write_vacancies_db\n{er}')


# Получаем Вакансии 
def get_vacancies(PARAMS, count):
    global count_vac_write
    count_vac_write += count
    pages = (count // 100) if count < 2000 else 20
    if pages == 0: pages = 1
    for page in range(0, pages):
        PARAMS.update({'per_page': 100, 'page': page})
        _, reception = get_requests(PARAMS)
        if reception:
            result_list  = parsing_vacancies_id_list(reception)
            write_vacancies_db(result_list)


# Из готовоого запроса json парсим id вакансий
def parsing_vacancies_id_list(reception_j):
    vacancies_id_list = []
    try:
        for vacancy in reception_j['items']:
            id = (vacancy['id'],)
            vacancies_id_list.append(id)
    except KeyError as er:
        print(f'Ошибка parsing_vacancies_id_list\n{er}')
    return vacancies_id_list



def get_specialization():
    '''
    Пробегаем по всем специальностям если вакансий в специальности меньше 2к отправляет на запись
    Если больше 2к формирует список и возвращает ID таких специальностей
    '''
    spec_list_more         = []
    specialization_id_list = get_specialization_list()
    for id in specialization_id_list:        
        PARAMS = {
            'specialization'  : id,
            'only_with_salary': True
        }
        count_vac, _   = get_requests(PARAMS)
        if count_vac   > 2_000:
            spec_list_more.append(id)
        else:
            print(f'На запись: {id=}, {count_vac=}')
            get_vacancies(PARAMS, count_vac)
    return spec_list_more


def get_specialization_and_industry(spec_list):
    # Специальность + индустрия + компания
    more_list       = []
    industries_list = get_industries_list()
    # other_list = set(spec_list) - result_set
    for spec_id in spec_list:
        for indus_id in industries_list:
            PARAMS = {
                'industry'        : indus_id,
                'specialization'  : spec_id,
                'only_with_salary': True
            }            
            count_vac, _ = get_requests(PARAMS)
            if count_vac > 2000:
                more_list.append((spec_id, indus_id))
            else:
                print(f'На запись: {spec_id=}, {indus_id=} {count_vac=}')
                get_vacancies(PARAMS, count_vac)
    return more_list


def get_SID(spec_indus_list):
    i = 0
    # Специальность + индустрия + дни
    for spec, indus in spec_indus_list:
        i += 1
        print(f'{spec=}, {indus=} : {i=}')  
        for day in range(0, 31):
            date_from = str(dt.date.today() - dt.timedelta(days=day))
            date_to   = str(dt.date.today() - dt.timedelta(days=day -1))
            PARAMS = {
                'date_from'         : date_from,
                'date_to'           : date_to,
                'specialization'    : spec,
                'industry'          : indus,
                'only_with_salary'  : True
            }
            count_vac, _  = get_requests(PARAMS)
            if count_vac != 0:                
                get_vacancies(PARAMS, count_vac)

            
def get_requests(PARAMS):
    try:
        reception      = requests.get(url=URL, headers=HEADERS, params=PARAMS)            
        reception_json = reception.json()
        if reception_json.get('errors'):
            use_selenium.update_ip_address() # меняем Ip address
        else:
            count_vac = reception_json['found']

    except Exception as er:
        count_vac, reception_json = 0, None
        print(f'Ошибка def get_requests\n{er}')

    return count_vac, reception_json


if __name__ == '__main__':
    # фильтр специализации, если находит меньше 2к вакансий забираем ID вакансий,
    # Возвращаем список ID специализаций у которых больше 2к вакансий
    data  = get_specialization()
    # фильтр специализации и индустрия компании, делам все то-же что и на прошлом шагу
    data2 = get_specialization_and_industry(data)
    # добавляем фильтр по дате публикации вакансии
    get_SID(data2)
    print('Работу завершил. Записал:', count_vac_write)    
    db.close()