import sqlite3


def uniq_id_employers():
    cursor.execute('''
        SELECT DISTINCT(employer_id), employer_name
        FROM vacancies
        WHERE employer_id not NULL
        ORDER BY employer_id
    ''')
    return cursor.fetchall()

def uniq_id_employers():
    cursor.execute('''
        SELECT id, employer_id, employer_name
        FROM vacancies
        WHERE employer_id is NULL
    ''')
    return cursor.fetchall()

def write_db(line):
    try:
        cursor.execute('INSERT INTO employers VALUES(?, ?)', line)
        db.commit()
    except Exception as ex:
        print(line, ex)

def update_vac(vac_id, emp_id):
    cursor.execute(f'''
        UPDATE vacancies
        SET employer_id = {emp_id} 
        WHERE id = {vac_id}
    ''')
    db.commit()

def enumeration_uniq_id(data):
    for el in data:
        write_db(el)

def enumeration_null_id(data):
    id = 6_040_000
    for vac_id, _, name in data:
        id += 1
        line = (id, name)
        write_db(line)
        update_vac(vac_id, id)



if __name__ == '__main__':
    db     = sqlite3.connect('VacanciesDB.db')
    cursor = db.cursor()
    # data   = uniq_id_employers()
    # enumeration_uniq_id(data)
    # data   = uniq_id_employers()
    # enumeration_null_id(data)
