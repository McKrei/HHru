

dict_currency = {
    'AZN': 44.29,
    'BYR': 29.5,
    'EUR': 86.15,
    'GEL': 25.42,
    'KGS': 0.89,
    'KZT': 0.18,
    'RUR': 1,
    'UAH': 2.67,
    'USD': 75.76,
    'UZS': 0.007
}

# Считаем ЗП
def caunting_salary(salary_from, salary_to, currency, gross):
    if salary_from:
        to_result = salary_from + salary_to / 2 if salary_to else salary_from
    elif salary_to:
        to_result = salary_to
    else:
        return 0
    if currency:
        to_result *= dict_currency[currency]
    if gross:
        to_result  = to_result if gross == False else to_result * 0.87
    return to_result

def finding_name(v_json, find, find_two='name'):
    try:
        if find == 'professional_roles':
            result = v_json[find][0][find_two]
        else:
            result = v_json[find][find_two]
    except KeyError:
        result = None
    return result


def table_vacancy_data(vacancy_j):
    id            = vacancy_j['id']
    name          = vacancy_j['name']
    area          = finding_name(vacancy_j, 'area')
    salary_d      = vacancy_j['salary']
    salary_from   = salary_d.get('from')
    salary_to     = salary_d.get('to')
    currency      = salary_d.get('currency')
    gross         = salary_d.get('gross')
    salary        = caunting_salary(salary_from, salary_to, currency, gross)
    work_address  = salary_d.get('address')
    experience    = finding_name(vacancy_j, 'experience')
    schedule      = finding_name(vacancy_j, 'schedule')
    employment    = finding_name(vacancy_j, 'employment')
    prof_roles    = finding_name(vacancy_j, 'professional_roles')
    employer_id   = finding_name(vacancy_j, 'employer', 'id')
    employer_name = finding_name(vacancy_j, 'employer')
    result = (
        id,
        name,
        area,
        salary_from,
        salary_to,
        currency,
        gross,
        salary,
        work_address,
        experience,
        schedule,
        employment,
        prof_roles,
        employer_id,
        employer_name
    )
    return result

def table_key_skills_data(vacancy_j):
    result_list     = []
    id              = vacancy_j['id']
    key_skills_list = vacancy_j.get('key_skills')

    if key_skills_list:

        for skill in key_skills_list:
            try:
                couple = (id, skill['name'])
                result_list.append(couple)
            except Exception:
                pass

    return result_list

def table_description_data(vacancy_j):
    id = vacancy_j['id']
    try:
        description = vacancy_j['description']
        return (id, description)
    except Exception:
        return (id, None)

def table_specializations_vacancies_data(vacancy_j):
    result_list     = []
    id_vacancy      = vacancy_j['id']
    specializations = vacancy_j.get('specializations')
    if specializations:
        for spec in specializations:
            try:
                id_spec = spec['id']
                result_list.append((id_vacancy, id_spec))
            except Exception as ex:
                pass
        
    return result_list

def main(data_json):
    if not data_json:
        return 'Нет данных'
    # создаем хранилища данных для таблиц
    vacancies_for_recording                 = []
    key_skills_for_recording                = []
    description_for_recording               = []
    specializations_vacancies_for_recording = []    
    
    for vacancy in data_json:
        try:
            vacancies_for_recording.append(\
                table_vacancy_data(vacancy)
            )
            spam = table_key_skills_data(vacancy)            
            key_skills_for_recording += spam

            description_for_recording.append(\
                table_description_data(vacancy)
            )
            spam = table_specializations_vacancies_data(vacancy)
            specializations_vacancies_for_recording += spam
            
        except Exception as er:
            print('main in parsing_json\n', er)
    return vacancies_for_recording,\
           key_skills_for_recording,\
           description_for_recording,\
           specializations_vacancies_for_recording


if __name__ == '__main__':
    pass
    # import requests
    # URL            = f'https://api.hh.ru/vacancies/8184005'
    # reception      = requests.get(url=URL)
    # reception_json = []
    # reception_json.append(reception.json())
    # a, b, c, d = main(reception_json)
    # breakpoint()