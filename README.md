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