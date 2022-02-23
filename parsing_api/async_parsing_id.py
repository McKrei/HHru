import time
import sqlite3
import aiohttp
import asyncio
from fake_useragent import UserAgent

import parsing_json
import use_selenium

start_time = time.time()
db         = sqlite3.connect('VacanciesDB.db')
cursor     = db.cursor()
update_ip  = False


# Получаем из БД 1000 ID вакансий
def geting_1000_id(start, limit):
    cursor.execute(f'''
        SELECT *
        FROM uniq_id
        EXCEPT
        SELECT id
        FROM vacancies
        -- SELECT *
        -- FROM   uniq_id
        -- ORDER  BY id
        LIMIT  {limit}
        OFFSET {start}
    ''')    
    return cursor.fetchall()

async def get_page_data(session, id: int):
    global update_ip
    URL = f'https://api.hh.ru/vacancies/{id[0]}'
    async with session.get(URL) as resp:
        try:
            assert resp.status == 200      
        except Exception as ex:
            pass
            # print('Ошибка подключения', ex)          
        resp_json = await resp.json()
        if resp_json.get('errors'):
            type_er = resp_json['errors'][0]['type']
            if type_er == 'captcha_required':
                update_ip = True
            elif type_er == "not_found":
                # print('Не нашел вакансии', id)
                pass
            else:
                print('geting_json спарсил ошибку', type_er, id)
            return
        data_json.append(resp_json)
        return resp_json



async def load_site_data(list_id):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for id in list_id:
            task = asyncio.create_task(get_page_data(session, id))
            tasks.append(task)
        await asyncio.gather(*tasks)


def write_db_data(t_vac, t_key, t_des, t_spe_vac):
    try:
        if t_vac:
            cursor.executemany('''
                INSERT INTO vacancies 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', t_vac)
        if t_key:
            cursor.executemany('''
                INSERT INTO key_skills 
                VALUES(?,?)''', t_key)
        if t_des:
            cursor.executemany('''
                INSERT INTO description
                VALUES(?,?)''', t_des)
        if t_spe_vac:
            cursor.executemany('''
                INSERT INTO specializations_vacancies 
                VALUES(?,?)''', t_spe_vac)
        db.commit()
    except Exception as er:
        print(f'write_db_data\n{er}')


    
def main(start, end, limit):
    global HEADERS, data_json, update_ip
    HEADERS = {'user-agent': UserAgent().random}
    i = 0
    while start < end:
        data_json = []
        list_id   = geting_1000_id(start, limit)
        try:
            asyncio.get_event_loop().run_until_complete(load_site_data(list_id))
            write_db_data(*parsing_json.main(data_json))
            start += limit
        except Exception as er:
            print('main', er)
            if update_ip == True:
                use_selenium.update_ip_address()
                update_ip = False

        print(f'Записал {start}')
        i += 1
        if i %100 == 0:
            HEADERS = {'user-agent': UserAgent().random}
            print(f'Записал {(time.time() - start_time) / 60} мин.')

        
if __name__ == '__main__':
    main(510500, 4300, 10)
    db.close()
    print(f'Записал {(time.time() - start_time) / 60} мин.')

# 3
# 540_178
