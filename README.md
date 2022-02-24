## Задачи:
+ Проанализировать данные на сайте ХХ ру
+ Поcтроить дашбор которым будет удобно пользовать на сайте
+ Ключевые таблицы, навыки, которые ищут работодатели и естественно ЗП

### Парсинг данных: 
У HHru есть отличное API которым я и пользовался. Однако есть 3-и проблемы: 
1. Без регистрации приложения у них на сайте, каждые 3-5 тыс. запросов блокируют  IP соединения. 
    + Обошел с помощью, динамического IP. Программно при возникновение ошибки через selenium перезагружал шлюз. файл use_selenium.py
2. При одном фильтре дает возможность посмотреть только 2к вакансий, когда нужно спарсить 1кк, это прям грустно!
    + Пришлось менять запросы подробнее в main.py
3. Есть лимиты на скорость запросов, у меня получилось асинхронно создавать только 50 задач, если увеличить будут проскакивать ошибки!

## Данные спарсил, что получилось! 

Получил 800к вакансий, и 3гб данных. 

Сейчас на стадии написания сайта с дашбордом. Примеры в папке schem.

Проект на паузе из-за хакатона, если есть вопросы пишите https://t.me/mckrei 
