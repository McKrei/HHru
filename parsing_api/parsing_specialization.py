import requests
import sqlite3

db     = sqlite3.connect('VacanciesDB.db')
cursor = db.cursor()


# Заполняем данными таблицу specializations! 
def specializations_table():
    URL            = 'https://api.hh.ru/specializations'
    reception      = requests.get(URL)
    reception_json = reception.json()
    result_data    = []

    for profarea in reception_json:
        profarea_id   = profarea['id']
        profarea_name = profarea['name']
        result_data.append((profarea_id, profarea_name, None))
        for spec in profarea['specializations']:
            id   = spec['id']
            name = spec['name']
            result_data.append((id, name, profarea_id))

    cursor.executemany('INSERT INTO specializations VALUES(?, ?, ?)', result_data)
    db.commit()



if __name__ == '__main__':

    db.close()