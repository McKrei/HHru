import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

db = sqlite3.connect('VacanciesDB.db')
cursor = db.cursor()

def key_skills(name):
    l_name = name.lower()
    t_name = name.capitalize()
    cursor.execute(f'''
        SELECT skill_name, count(t1.id) as count_skill
        FROM(
            SELECT id
            FROM vacancies
            WHERE name LIKE "%Аналитик%" or "%аналитик%"
            UNION
            SELECT vacancy_id
            FROM description
            WHERE description LIKE "%Аналитик%" or "%аналитик%"
        ) as t1
        JOIN key_skills as t2
        ON t1.id = t2.vacancy_id
        GROUP BY skill_name
        ORDER BY count_skill DESC
        LIMIT 20
    ''')
    data_skills = cursor.fetchall()
    if not data_skills:
        print('Не нашел', name)
        return
    df = pd.DataFrame(data_skills)
    
    df.sort_values(by=1).plot.barh(
                x=0, 
                y=1,
                figsize=(15, 7),
                title='ТОП20'
    )
    plt.show()
    # plt.savefig('save.png')

def salary_experience(name):
    l_name = name.lower()
    t_name = name.capitalize()
    cursor.execute(f'''
        SELECT experience, avg(salary) as avg_salary
        FROM(
            SELECT id
            FROM vacancies
            WHERE name LIKE "%Аналитик%" or "%аналитик%"
            UNION
            SELECT vacancy_id as id
            FROM description
            WHERE description LIKE "%Аналитик%" or "%аналитик%"
        ) as t1
        JOIN vacancies as t2 
        ON t1.id = t2.id
        GROUP BY experience
    ''')
    data_experience = cursor.fetchall()
    df = pd.DataFrame(data_experience, columns=['Experience', 'Salary'])


if __name__ == '__main__':
    name = 'Аналитик данных'
    # key_skills(name)
    salary_experience(name)