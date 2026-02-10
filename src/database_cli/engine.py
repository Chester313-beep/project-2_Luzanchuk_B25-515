import os
import sys

from prettytable import PrettyTable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from core import (
        create_table,
        delete,
        drop_table,
        get_table_info,
        insert,
        list_tables,
        select,
        update,
    )
    from parser import (
        parse_create,
        parse_delete,
        parse_drop,
        parse_info,
        parse_insert,
        parse_select,
        parse_update,
    )
    from utils import save_metadata
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    sys.exit(1)


def display_welcome():
    print("=" * 60)
    print("Добро пожаловать в систему управления базой данных!")
    print("=" * 60)
    print("\n***Операции с таблицами***\n")
    print("Функции:")
    print("<command> create <имя_таблицы> (<столбец1 тип1>, ...)")
    print("<command> drop <имя_таблицы> - удалить таблицу.")
    print("<command> list - вывести список всех таблиц.")
    print("\n***Операции с данными***\n")
    print("Функции:")
    print("<command> insert <имя_таблицы> values (<значение1>, ...) - создать запись.")
    print("<command> select <имя_таблицы> where <столбец> = <значение>")
    print("<command> select <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия>"
    )
    print("<command> delete <имя_таблицы> where <столбец> = <значение>")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> exit - выход из программы")
    print("\nПримеры команд:")
    print("create users (ID int, Name str, Age int)")
    print("insert users values (1, 'Иван', 25)")
    print("select users where Age = 25")
    print("update users set Age = 26 where ID = 1")
    print("=" * 60)


def display_table(data):
    if not data:
        print("Нет данных для отображения")
        return

    table = PrettyTable()
    table.field_names = data[0].keys()

    for record in data:
        row = []
        for key in table.field_names:
            row.append(record.get(key, ""))
        table.add_row(row)

    print(table)


def execute_command(command: str, metadata: dict) -> bool:
    lower_command = command.lower().strip()

    if lower_command == "exit":
        print("Выход из программы.")
        return False
    elif lower_command == "help":
        display_welcome()
        return True
    elif lower_command == "list":
        result = list_tables(metadata)
        if result is None:
            return True
        if result:
            print("Список таблиц:")
            for table in result:
                print(f"  - {table}")
        else:
            print("Нет созданных таблиц.")
        return True

    try:
        if lower_command.startswith("create"):
            table_name, columns = parse_create(command)
            result = create_table(metadata, table_name, columns)
            if result is None:
                return True
            try:
                save_metadata(result)
                print(f"Таблица '{table_name}' успешно создана.")
            except Exception as e:
                print(f"Ошибка при сохранении метаданных: {e}")
                return True

        elif lower_command.startswith("drop"):
            table_name = parse_drop(command)
            result = drop_table(metadata, table_name)
            if result is None:
                return True
            try:
                save_metadata(result)
                print(f"Таблица '{table_name}' успешно удалена.")
            except Exception as e:
                print(f"Ошибка при сохранении метаданных: {e}")
                return True

        elif lower_command.startswith("insert"):
            table_name, values = parse_insert(command)
            result = insert(metadata, table_name, values)
            if result is None:
                return True
            print(
                f"Запись с ID={result['id']} успешно добавлена "
                f"в таблицу '{table_name}'."
            )

        elif lower_command.startswith("select"):
            table_name, where_clause = parse_select(command)
            result = select(metadata, table_name, where_clause)
            if result is None:
                return True
            if result["data"]:
                display_table(result["data"])
                print(f"Найдено записей: {result['count']}")
            else:
                print("Записи не найдены.")

        elif lower_command.startswith("update"):
            table_name, set_clause, where_clause = parse_update(command)
            result = update(metadata, table_name, set_clause, where_clause)
            if result is None:
                return True
            if result["count"] > 0:
                ids_str = ", ".join(map(str, result["ids"]))
                print(
                    f"Записи с ID=[{ids_str}] в таблице "
                    f"'{table_name}' успешно обновлены."
                )
            else:
                print("Нет записей, соответствующих условию.")

        elif lower_command.startswith("delete"):
            table_name, where_clause = parse_delete(command)
            result = delete(metadata, table_name, where_clause)
            if result is None:
                return True
            if result["count"] > 0:
                ids_str = ", ".join(map(str, result["ids"]))
                print(
                    f"Записи с ID=[{ids_str}] успешно "
                    f"удалены из таблицы '{table_name}'."
                )
            else:
                print("Нет записей, соответствующих условию.")

        elif lower_command.startswith("info"):
            table_name = parse_info(command)
            result = get_table_info(metadata, table_name)
            if result is None:
                return True
            print(f"Информация о таблице '{table_name}':")
            print(f"  Столбцы: {result['columns']}")
            print(f"  Количество записей: {result['record_count']}")

        else:
            print("Неизвестная команда. Введите 'help' для справки.")

    except Exception as e:
        print(f"Ошибка выполнения команды: {e}")

    return True
