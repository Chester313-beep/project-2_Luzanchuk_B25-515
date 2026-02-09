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

```asciinema
<script id="asciicast-XXXXXX" src="https://asciinema.org/a/XXXXXX.js" async></script>
```

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