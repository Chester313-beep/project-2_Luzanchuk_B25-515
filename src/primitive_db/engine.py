import shlex

from .core import create_table, describe_table, drop_table, list_tables
from .utils import load_metadata, save_metadata


def run() -> None:
    print("Добро пожаловать в Primitive Database!")
    print("=" * 50)
    print("Доступные команды:")
    print("  create <table_name> <col1:type> <col2:type> ...")
    print("      Создать таблицу")
    print("  drop <table_name>")
    print("      Удалить таблицу")
    print("  list")
    print("      Показать все таблицы")
    print("  describe <table_name>")
    print("      Описание таблицы")
    print("  help")
    print("      Показать справку")
    print("  exit")
    print("      Выйти из программы")
    print("=" * 50)
    METADATA_FILE = "db_meta.json"
    while True:
        try:
            user_input = input("\n>>> ").strip()
            if not user_input:
                continue
            try:
                parts = shlex.split(user_input)
            except ValueError as e:
                print(f"Ошибка разбора команды: {e}")
                continue
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            metadata = load_metadata(METADATA_FILE)
            if command == "exit":
                print("Выход из программы. До свидания!")
                break
            elif command == "help":
                print("\nДоступные команды:")
                print("  create <table_name> <col1:type> <col2:type> ...")
                print("      Создать новую таблицу.")
                print("      Автоматически добавляет столбец ID:int")
                print("      Пример: create users name:str age:int email:str")
                print("      Допустимые типы: int, str, bool")
                print("\n  drop <table_name>")
                print("      Удалить таблицу")
                print("      Пример: drop users")
                print("\n  list")
                print("      Показать список всех таблиц")
                print("\n  describe <table_name>")
                print("      Показать структуру таблицы")
                print("      Пример: describe users")
                print("\n  help")
                print("      Показать эту справку")
                print("\n  exit")
                print("      Выйти из программы")
            elif command == "create":
                if len(args) < 2:
                    print("Ошибка: недостаточно аргументов")
                    usage = "Использование: create <table_name> <col1:type> ..."
                    print(usage)
                    continue
                table_name = args[0]
                columns = args[1:]
                try:
                    metadata = create_table(metadata, table_name, columns)
                    save_metadata(METADATA_FILE, metadata)
                    print(f"Таблица '{table_name}' успешно создана!")
                    print(f"Столбцы: {metadata[table_name]['columns']}")
                except ValueError as e:
                    print(f"Ошибка: {e}")
            elif command == "drop":
                if len(args) != 1:
                    print("Ошибка: неверное количество аргументов")
                    print("Использование: drop <table_name>")
                    continue
                table_name = args[0]
                confirm_msg = (
                    f"Вы уверены, что хотите удалить таблицу '{table_name}'? "
                    "(y/N): "
                )
                confirm = input(confirm_msg).strip().lower()
                if confirm != 'y':
                    print("Удаление отменено")
                    continue
                try:
                    metadata = drop_table(metadata, table_name)
                    save_metadata(METADATA_FILE, metadata)
                    print(f"Таблица '{table_name}' успешно удалена!")
                except ValueError as e:
                    print(f"Ошибка: {e}")
            elif command == "list":
                tables = list_tables(metadata)
                if not tables:
                    print("В базе данных нет таблиц")
                else:
                    print(f"Найдено таблиц: {len(tables)}")
                    print("-" * 30)
                    for i, table_name in enumerate(tables, 1):
                        table_info = metadata[table_name]
                        print(f"{i}. {table_name}")
                        print(f"   Столбцов: {len(table_info['columns'])}")
                        print(f"   Строк: {table_info.get('row_count', 0)}")
                        print() 
            elif command == "describe":
                if len(args) != 1:
                    print("Ошибка: неверное количество аргументов")
                    print("Использование: describe <table_name>")
                    continue
                table_name = args[0]
                table_info = describe_table(metadata, table_name)
                if table_info is None:
                    print(f"Таблица '{table_name}' не найдена")
                else:
                    print(f"Таблица: {table_name}")
                    print(f"Первичный ключ: {table_info.get('primary_key', 'ID')}")
                    print(f"Количество строк: {table_info.get('row_count', 0)}")
                    print("\nСтолбцы:")
                    print("-" * 30)
                    for column in table_info['columns']:
                        col_name, col_type = column.split(':', 1)
                        is_pk = col_name == table_info.get('primary_key')
                        pk_marker = " (PK)" if is_pk else ""
                        print(f"  {col_name}: {col_type}{pk_marker}") 
            elif command == "clear":
                print("\n" * 100)
            else:
                print(f"Неизвестная команда: '{command}'")
                print("Введите 'help' для просмотра доступных команд")
        except KeyboardInterrupt:
            print("\n\nВыход из программы. До свидания!")
            break
        except EOFError:
            print("\n\nВыход из программы. До свидания!")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            print("Пожалуйста, сообщите об этом разработчику")