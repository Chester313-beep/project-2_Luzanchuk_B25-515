# Primitive Database

Простая реляционная база данных с CLI интерфейсом, написанная на Python.

## Установка

### Установка из PyPI
```bash
pip install primitive-db
```

### Установка из исходного кода
```bash
git clone https://github.com/Chester313-beep/project-2_Luzanchuk_B25-515.git
cd primitive-db
poetry install
```

## Управление таблицами

### Создание таблицы
```
create <table_name> <col1:type> <col2:type> ...
```
- Автоматически добавляет столбец `ID:int` в качестве первичного ключа
- Допустимые типы: `int`, `str`, `bool`

**Пример:**
```sql
>>> create users name:str age:int email:str
Таблица 'users' успешно создана!
Столбцы: ['ID:int', 'name:str', 'age:int', 'email:str']
```

### Удаление таблицы
```
drop <table_name>
```

**Пример:**
```sql
>>> drop users
Вы уверены, что хотите удалить таблицу 'users'? (y/N): y
Таблица 'users' успешно удалена!
```

### Просмотр списка таблиц
```
list
```

**Пример:**
```sql
>>> list
Найдено таблиц: 2
------------------------------
1. users
   Столбцов: 4
   Строк: 0

2. products
   Столбцов: 3
   Строк: 0
```

### Описание таблицы
```
describe <table_name>
```

**Пример:**
```sql
>>> describe users
Таблица: users
Первичный ключ: ID
Количество строк: 0

Столбцы:
------------------------------
  ID: int (PK)
  name: str
  age: int
  email: str
```

### Справка
```
help
```

### Выход
```
exit
```

## Пример использования

## Разработка

### Установка для разработки
```bash
git clone https://github.com/Chester313-beep/project-2_Luzanchuk_B25-515.git
cd primitive-db
poetry install
poetry run database
```

### Запуск тестов
```bash
poetry run pytest
```

### Форматирование кода
```bash
poetry run ruff format .
poetry run ruff check --fix .
```

## Структура проекта
```
primitive-db/
├── src/
│   └── primitive_db/
│       ├── __init__.py
│       ├── main.py          # Точка входа
│       ├── engine.py        # Основной цикл программы
│       ├── core.py          # Логика работы с таблицами
│       └── utils.py         # Утилиты для работы с JSON
├── pyproject.toml
├── README.md
└── db_meta.json             # Файл метаданных (создается автоматически)
```

## Лицензия
MIT License. Подробнее см. в файле LICENSE.

## Database CLI
Простая реляционная база данных с командной строкой, поддерживающая полный набор CRUD-операций.

## Установка
## Установка через pip
```bash
pip install database-cli
```
## Установка из исходного кода
```bash
git clone <репозиторий>
cd database-cli
poetry install
poetry build
pip install dist/database_cli-*.whl
```
## Использование
## После установки запустите базу данных командой:

``` bash
database
```
## Вы увидите приветственное сообщение с описанием доступных команд.

## CRUD-операции
1. Добавление записей (Create)
sql
insert into <имя_таблицы> values (<значение1>, <значение2>, ...)
**Примеры:**

``` bash
>>> insert into users values ("Иван", 25, true)
Запись с ID=1 успешно добавлена в таблицу "users".

>>> insert into products values ("Ноутбук", 999.99, 10)
Запись с ID=1 успешно добавлена в таблицу "products".
```
2. Чтение записей (Read)
sql
-- Все записи
select from <имя_таблицы>

-- С фильтрацией
select from <имя_таблицы> where <столбец> = <значение>
Примеры:

```bash
>>> select from users
+----+--------+-----+-----------+
| ID |  name  | age | is_active |
+----+--------+-----+-----------+
| 1  | Иван   | 25  |   True    |
| 2  | Мария  | 30  |   True    |
| 3  | Петр   | 28  |   False   |
+----+--------+-----+-----------+

>>> select from users where age = 25
+----+-------+-----+-----------+
| ID | name  | age | is_active |
+----+-------+-----+-----------+
| 1  | Иван  | 25  |   True    |
+----+-------+-----+-----------+
```
3. Обновление записей (Update)
sql
update <имя_таблицы> 
set <столбец1> = <новое_значение1>, <столбец2> = <новое_значение2> 
where <условие>
**Примеры:**

```bash
>>> update users set age = 26 where name = "Иван"
Записи с ID=[1] в таблице "users" успешно обновлены.

>>> update products set price = 899.99, stock = 15 where ID = 1
Записи с ID=[1] в таблице "products" успешно обновлены.
```
4. Удаление записей (Delete)
sql
delete from <имя_таблицы> where <условие>
**Примеры:**

```bash
>>> delete from users where ID = 3
Записи с ID=[3] успешно удалены из таблицы "users".

>>> delete from products where stock = 0
Записи с ID=[5,7,9] успешно удалены из таблицу "products".
```
5. Информация о таблице
bash
info <имя_таблицы>
**Пример:**

```bash
>>> info users
Таблица: users
Столбцы: ID:int, name:str, age:int, is_active:bool
Количество записей: 2
```
Управление таблицами
Создание таблицы
```bash
create table <имя> (<столбец1:тип>, <столбец2:тип>, ...)
```
```bash
>>> create table users (name:str, age:int, is_active:bool)
Таблица 'users' успешно создана.
```
## Удаление таблицы
```bash
drop table <имя>
```
## Просмотр таблиц
```bash
show tables
```
## Текстовая демонстрация сессии
```bash
database
```
***Операции с данными***

>>> create table employees (name:str, position:str, salary:float, active:bool)
Таблица 'employees' успешно создана.

>>> insert into employees values ("Алексей", "Разработчик", 150000.0, true)
Запись с ID=1 успешно добавлена в таблицу "employees".

>>> insert into employees values ("Ольга", "Дизайнер", 120000.0, true)
Запись с ID=2 успешно добавлена в таблицу "employees".

>>> select from employees
+----+----------+--------------+----------+--------+
| ID |   name   |   position   |  salary  | active |
+----+----------+--------------+----------+--------+
| 1  | Алексей  | Разработчик  | 150000.0 |  True  |
| 2  |  Ольга   |   Дизайнер   | 120000.0 |  True  |
+----+----------+--------------+----------+--------+

>>> update employees set salary = 160000.0 where name = "Алексей"
Записи с ID=[1] в таблице "employees" успешно обновлены.

>>> select from employees where position = "Разработчик"
+----+----------+--------------+----------+--------+
| ID |   name   |   position   |  salary  | active |
+----+----------+--------------+----------+--------+
| 1  | Алексей  | Разработчик  | 160000.0 |  True  |
+----+----------+--------------+----------+--------+

>>> info employees
Таблица: employees
Столбцы: ID:int, name:str, position:str, salary:float, active:bool
Количество записей: 2

>>> show tables
Существующие таблицы:
  - employees

>>> exit
Выход из программы...

## Модуль декораторов (src/decorators.py)
## Обзор
Модуль decorators.py содержит набор декораторов для улучшения функциональности и безопасности операций с базой данных. Все декораторы реализованы с использованием стандартной библиотеки Python и следуют лучшим практикам проектирования.

## Установка и использование
python
# Импорт всех декораторов
```bash
from src.decorators import (
    handle_db_errors,
    confirm_action,
    log_time,
    create_cacher,
)
```
# Создание кэшера
```bash
cache_result = create_cacher()
```
## Декораторы
1. @handle_db_errors
Назначение: Универсальная обработка исключений при работе с базой данных.

Обрабатываемые исключения:

KeyError - обращение к несуществующей таблице или ключу

ValueError - ошибки валидации типов данных

FileNotFoundError - отсутствие файлов базы данных

Exception - любые другие исключения

**Пример использования:**
```bash
python
@handle_db_errors
def database_operation(table_name):
    if table_name not in self.tables:
        raise KeyError(f"Таблица {table_name} не найдена")
    # остальная логика...
```
## Результат при ошибке:
```bash
Ошибка: таблица или ключ не найдены - Таблица users не найдена
```
2. @confirm_action(action_name)
Назначение: Запрос подтверждения у пользователя перед выполнением опасных операций.

**Параметры:**

action_name (str): Название операции для отображения в запросе

**Пример использования:**
```bash
python
@confirm_action("удаление таблицы")
def drop_table(table_name):
    print(f"Таблица {table_name} удалена")
```
**Интерактивное поведение:**
```bash
Вы уверены, что хотите выполнить "удаление таблицы"? [y/n]: n
Операция отменена.
```
3. @log_time
# Назначение: Замер времени выполнения функции.

**Пример использования:**
```bash
python
@log_time
def select_complex_query(conditions):
    time.sleep(1)
    return results
```
**Вывод:**
```bash
Функция select_complex_query выполнилась за 1.234 секунд
```
4. create_cacher()
# Назначение: Фабрика функций для кэширования результатов операций.

Возвращает: Функцию cache_result(key, value_func)

**Пример использования:**
```bash
python
cache_result = create_cacher()

def select_with_cache(table_name, condition):
    cache_key = f"select_{table_name}_{condition}"
    
    return cache_result(
        key=cache_key,
        value_func=lambda: execute_expensive_query(table_name, condition)
    )
```
**Поведение:**

Первый вызов: Результат закэширован с ключом: select_users_age_25

Последующие вызовы: Используется кэшированный результат для ключа: select_users_age_25

# Комплексное применение
**Пример объединения декораторов:**
```bash
python
class Database:
    @log_time
    @handle_db_errors
    def select(self, table_name, condition=None):
        """Замер времени + обработка ошибок"""
        cache_key = f"select_{table_name}_{condition}"
        
        return cache_result(
            cache_key,
            lambda: self._execute_select(table_name, condition)
        )
    
    @confirm_action("удаление таблицы")
    @handle_db_errors
    def drop_table(self, table_name):
        """Подтверждение + обработка ошибок"""
        if table_name not in self.tables:
            raise KeyError(f"Таблица {table_name} не найдена")
Порядок применения декораторов
Декораторы применяются снизу вверх:

python
@decorator3
@decorator2
@decorator1
def function():
    pass
```
