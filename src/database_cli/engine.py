import sys
import os
from prettytable import PrettyTable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from core import (
        create_table,
        drop_table, 
        list_tables,
        describe_table,
        insert,
        select,
        update,
        delete,
        get_table_info
    )
    from utils import load_metadata, save_metadata, load_table_data, save_table_data, convert_to_type
    from parser import CommandParser
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что все файлы находятся в той же директории:")
    print("  - core.py")
    print("  - utils.py")
    print("  - parser.py")
    sys.exit(1)


def display_welcome():
    print("database")
    print("\n***Операции с данными***\n")
    print("Функции:")
    print("<command> insert <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.")
    print("<command> select <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")
    print("<command> select <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete <имя_таблицы> where <столбец> = <значение> - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")


def display_help():
    print("\nДоступные команды:")
    print("1. Создание таблиц:")
    print("   create table <имя_таблицы> (<столбец1>:<тип>, <столбец2>:<тип>, ...)")
    print("   drop table <имя_таблицы>")
    print("   show tables")
    print()
    print("2. CRUD операции:")
    print("   insert <таблица> values (<значение1>, <значение2>, ...)")
    print("   select <таблица> [where <условие>]")
    print("   update <таблица> set <столбец>=<значение> where <условие>")
    print("   delete <таблица> where <условие>")
    print("   info <таблица>")
    print()
    print("3. Системные:")
    print("   exit - выход")
    print("   help - эта справка")


def display_table(data, columns):
    if not data:
        print("Нет данных для отображения")
        return
    table = PrettyTable()
    table.field_names = columns  
    for record in data:
        row = []
        for col in columns:
            row.append(record.get(col, ""))
        table.add_row(row)
    table.align = "l"
    print(table)


def execute_command(command):
    command = command.strip()
    metadata = load_metadata()
    try:
        lower_command = command.lower()
        if lower_command.startswith("create table"):
            try:
                parts = command.split("create table")[1].strip()
                if '(' not in parts or ')' not in parts:
                    print("Ошибка: Неверный формат команды CREATE TABLE")
                    return False
                table_name, cols = parts.split('(', 1)
                table_name = table_name.strip()
                cols = cols.rstrip(')').strip()
                columns = [c.strip() for c in cols.split(',') if c.strip()]
                metadata = create_table(metadata, table_name, columns)
                save_metadata(metadata)
                print(f"Таблица '{table_name}' успешно создана.")
            except Exception as e:
                print(f"Ошибка создания таблицы: {e}")
        elif lower_command.startswith("drop table"):
            parts = command.split()
            if len(parts) != 3:
                print("Ошибка: Используйте: drop table <имя_таблицы>")
                return False
            table_name = parts[2]
            if table_name in metadata:
                metadata = drop_table(metadata, table_name)
                save_metadata(metadata)
                file_path = f"data/{table_name}.json"
                if os.path.exists(file_path):
                    os.remove(file_path)
                print(f"Таблица '{table_name}' успешно удалена.")
            else:
                print(f"Таблица '{table_name}' не существует.")
        elif lower_command == "show tables":
            tables = list_tables(metadata)
            if not tables:
                print("Нет созданных таблиц.")
            else:
                print("Существующие таблицы:")
                for table_name in tables:
                    print(f"  - {table_name}")
        elif lower_command.startswith("insert"):
            table_name, values = CommandParser.parse_insert(command)
            if table_name not in metadata:
                print(f"Ошибка: Таблица '{table_name}' не существует.")
                return False
            result = insert(metadata, table_name, values)
            print(f"Запись с ID={result['id']} успешно добавлена в таблицу '{table_name}'.")
        elif lower_command.startswith("select"):
            table_name, where_clause = CommandParser.parse_select(command)
            if table_name not in metadata:
                print(f"Ошибка: Таблица '{table_name}' не существует.")
                return False
            result = select(metadata, table_name, where_clause)
            if result:
                columns = list(metadata[table_name]["columns"].keys())
                display_table(result, columns)
            else:
                print("Нет записей, соответствующих условию.")
        elif lower_command.startswith("update"):
            table_name, set_clause, where_clause = CommandParser.parse_update(command)
            if table_name not in metadata:
                print(f"Ошибка: Таблица '{table_name}' не существует.")
                return False
            result = update(metadata, table_name, set_clause, where_clause)
            if result["count"] > 0:
                ids_str = ", ".join(map(str, result["ids"]))
                print(f"Записи с ID=[{ids_str}] в таблице '{table_name}' успешно обновлены.")
            else:
                print("Нет записей, соответствующих условию.")
        elif lower_command.startswith("delete"):
            table_name, where_clause = CommandParser.parse_delete(command)
            if table_name not in metadata:
                print(f"Ошибка: Таблица '{table_name}' не существует.")
                return False
            result = delete(metadata, table_name, where_clause)
            if result["count"] > 0:
                ids_str = ", ".join(map(str, result["ids"]))
                print(f"Записи с ID=[{ids_str}] успешно удалены из таблицы '{table_name}'.")
            else:
                print("Нет записей, соответствующих условию.")
        elif lower_command.startswith("info "):
            table_name = CommandParser.parse_info(command)
            if table_name not in metadata:
                print(f"Ошибка: Таблица '{table_name}' не существует.")
                return False
            info = get_table_info(metadata, table_name)
            print(f"\nТаблица: {info['name']}")
            print("Столбцы:", end=" ")
            columns_info = []
            for col_name, col_type in info['columns'].items():
                columns_info.append(f"{col_name}:{col_type}")
            print(", ".join(columns_info))
            print(f"Количество записей: {info['record_count']}")
        elif lower_command == "help":
            display_help()
        elif lower_command == "exit":
            print("Выход из программы...")
            return True
        else:
            print("Неизвестная команда. Введите 'help' для справки.")
    except Exception as e:
        print(f"Ошибка: {e}")
    return False
