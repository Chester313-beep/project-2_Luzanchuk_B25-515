import json
import os
from typing import Any, Dict, List, Optional


def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Ошибка в функции {func.__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None
    return wrapper


def confirm_action(action_name):
    def decorator(func):
        return func
    return decorator


def log_time(func):
    return func


def create_cacher():
    def cache_result(key, value_func):
        return value_func()
    return cache_result


try:
    from .utils import (
        convert_to_type,
        load_table_data,
        save_table_data,
    )
except ImportError:
    from utils import (
        convert_to_type,
        load_table_data,
        save_table_data,
    )

cache_result = create_cacher()


def create_database(db_name: str) -> Dict[str, Any]:
    return {
        'db_name': db_name,
        'tables': {},
    }


def get_table(db: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    if table_name not in db['tables']:
        raise KeyError(f"Таблица {table_name} не найдена")
    return db['tables'][table_name]


def set_table(
    db: Dict[str, Any],
    table_name: str,
    table_data: Dict[str, Any]
) -> Dict[str, Any]:
    db['tables'][table_name] = table_data
    return db


@handle_db_errors
def db_create_table(
    db: Dict[str, Any],
    table_name: str,
    columns: List[str]
) -> Dict[str, Any]:
    if table_name in db['tables']:
        raise ValueError(f"Таблица {table_name} уже существует")

    db['tables'][table_name] = {
        'columns': columns,
        'data': [],
        'next_id': 1,
    }
    print(f"Таблица '{table_name}' создана")
    return db


@confirm_action("удаление таблицы")
@handle_db_errors
def db_drop_table(db: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    if table_name not in db['tables']:
        raise KeyError(f"Таблица {table_name} не найдена")

    del db['tables'][table_name]
    print(f"Таблица '{table_name}' удалена")
    return db


@log_time
@handle_db_errors
def db_select(
    db: Dict[str, Any],
    table_name: str,
    condition=None,
    columns=None
) -> List[Dict[str, Any]]:
    cache_key = f"select_{table_name}_{str(condition)}_{str(columns)}"

    def execute_select():
        table = get_table(db, table_name)
        result = []

        for row in table['data']:
            if condition is None or condition(row):
                if columns is None:
                    result.append(row.copy())
                else:
                    filtered_row = {
                        col: row[col] for col in columns if col in row
                    }
                    result.append(filtered_row)

        return result

    return cache_result(cache_key, execute_select)


@log_time
@handle_db_errors
def db_insert(db: Dict[str, Any], table_name: str, data: Dict[str, Any]) -> int:
    table = get_table(db, table_name)

    for column in table['columns']:
        if column not in data:
            raise ValueError(f"Отсутствует обязательная колонка: {column}")

    data_with_id = data.copy()
    data_with_id['id'] = table['next_id']
    table['next_id'] += 1

    table['data'].append(data_with_id)
    print(f"Добавлена запись в таблицу '{table_name}' (ID: {data_with_id['id']})")
    return data_with_id['id']


@confirm_action("удаление записи")
@handle_db_errors
def db_delete(
    db: Dict[str, Any],
    table_name: str,
    condition
) -> int:
    table = get_table(db, table_name)
    initial_count = len(table['data'])

    table['data'] = [row for row in table['data'] if not condition(row)]

    deleted_count = initial_count - len(table['data'])
    print(f"Удалено {deleted_count} записей из таблицы '{table_name}'")
    return deleted_count


@handle_db_errors
def db_update(
    db: Dict[str, Any],
    table_name: str,
    condition,
    updates: Dict[str, Any]
) -> int:
    table = get_table(db, table_name)
    updated_count = 0

    for row in table['data']:
        if condition(row):
            row.update(updates)
            updated_count += 1

    print(f"Обновлено {updated_count} записей в таблице '{table_name}'")
    return updated_count


@handle_db_errors
def db_save_to_file(db: Dict[str, Any], filename: str) -> None:
    serializable_tables = {}
    for table_name, table_data in db['tables'].items():
        serializable_tables[table_name] = {
            'columns': table_data['columns'],
            'data': table_data['data'],
            'next_id': table_data['next_id'],
        }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(serializable_tables, f, indent=2, ensure_ascii=False)

    print(f"База данных сохранена в файл '{filename}'")


@handle_db_errors
def db_load_from_file(filename: str) -> Dict[str, Any]:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл {filename} не найден")

    with open(filename, 'r', encoding='utf-8') as f:
        serializable_tables = json.load(f)

    db = {
        'db_name': os.path.splitext(os.path.basename(filename))[0],
        'tables': serializable_tables,
    }
    print(f"База данных загружена из файла '{filename}'")
    return db


@handle_db_errors
def create_table(
    metadata: Dict[str, Any],
    table_name: str,
    columns: List[str],
) -> Dict[str, Any]:
    if table_name in metadata:
        raise ValueError(f"Таблица '{table_name}' уже существует")

    metadata[table_name] = {"columns": columns}
    return metadata


@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не найдена")

    del metadata[table_name]
    return metadata


@handle_db_errors
def list_tables(metadata: Dict[str, Any]) -> List[str]:
    return list(metadata.keys())


@handle_db_errors
def describe_table(
    metadata: Dict[str, Any],
    table_name: str,
) -> Optional[Dict[str, Any]]:
    return metadata.get(table_name)


@log_time
@handle_db_errors
def insert(
    metadata: Dict[str, Any],
    table_name: str,
    values: List[str],
) -> Dict[str, Any]:
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не найдена")

    table_info = metadata[table_name]

    if not isinstance(table_info, dict):
        raise ValueError(f"Метаданные таблицы '{table_name}' повреждены")

    if "columns" not in table_info:
        raise ValueError(
            f"Таблица '{table_name}' не содержит определения столбцов"
        )

    columns_list = table_info["columns"]
    if not isinstance(columns_list, list):
        raise ValueError(
            f"Определение столбцов в таблице '{table_name}' "
            "должно быть списком"
        )

    expected_count = len(columns_list)

    if len(values) != expected_count:
        raise ValueError(
            f"Неверное количество значений. Ожидается {expected_count}, "
            f"получено {len(values)}"
        )

    data = load_table_data(table_name)
    new_record = {}
    new_id = len(data) + 1

    for i, col_def in enumerate(columns_list):
        try:
            if not isinstance(col_def, str):
                raise ValueError(
                    f"Определение столбца должно быть строкой, "
                    f"получено: {type(col_def)}"
                )

            parts = col_def.split(" ")
            if len(parts) == 1:
                col_name = parts[0]
                col_type = "str"
            else:
                col_name = " ".join(parts[:-1])
                col_type = parts[-1]

            converted_value = convert_to_type(values[i], col_type)
            new_record[col_name] = converted_value
        except Exception as e:
            raise ValueError(f"Ошибка в столбце '{col_def}': {e}") from e

    data.append(new_record)
    save_table_data(table_name, data)

    return {"id": new_id}


@log_time
@handle_db_errors
def select(
    metadata: Dict[str, Any],
    table_name: str,
    where_clause: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не найдена")

    data = load_table_data(table_name)
    result = []
    matched_ids = []

    for record in data:
        match = True
        if where_clause:
            for column, value in where_clause.items():
                try:
                    if str(record.get(column, "")) != str(value):
                        match = False
                        break
                except Exception:
                    match = False
                    break

        if match:
            result.append(record)
            matched_ids.append(record.get("ID"))

    return {"data": result, "ids": matched_ids, "count": len(result)}


@handle_db_errors
def update(
    metadata: Dict[str, Any],
    table_name: str,
    set_clause: Dict[str, Any],
    where_clause: Dict[str, Any],
) -> Dict[str, Any]:
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не найдена")

    data = load_table_data(table_name)
    updated_ids = []
    table_info = metadata[table_name]

    for record in data:
        match = True
        for column, value in where_clause.items():
            try:
                if str(record.get(column, "")) != str(value):
                    match = False
                    break
            except Exception:
                match = False
                break

        if match:
            for column, new_value in set_clause.items():
                col_type = None
                for col_def in table_info["columns"]:
                    if col_def.startswith(column):
                        parts = col_def.split(" ")
                        if len(parts) == 1:
                            col_name_in_def = parts[0]
                            current_type = "str"
                        else:
                            col_name_in_def = " ".join(parts[:-1])
                            current_type = parts[-1]

                        if col_name_in_def == column:
                            col_type = current_type
                            break

                if col_type:
                    try:
                        converted_value = convert_to_type(new_value, col_type)
                        record[column] = converted_value
                    except Exception as e:
                        raise ValueError(
                            f"Ошибка обновления '{column}': {e}"
                        ) from e
                else:
                    record[column] = new_value

            updated_ids.append(record["ID"])

    if updated_ids:
        save_table_data(table_name, data)

    return {"ids": updated_ids, "count": len(updated_ids)}


@confirm_action("удаление записи")
@handle_db_errors
def delete(
    metadata: Dict[str, Any],
    table_name: str,
    where_clause: Dict[str, Any],
) -> Dict[str, Any]:
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не найдена")

    data = load_table_data(table_name)
    deleted_ids = []
    remaining_data = []

    for record in data:
        match = True
        if where_clause:
            for column, value in where_clause.items():
                try:
                    if str(record.get(column, "")) != str(value):
                        match = False
                        break
                except Exception:
                    match = False
                    break

        if match:
            deleted_ids.append(record.get("ID"))
        else:
            remaining_data.append(record)

    if deleted_ids:
        save_table_data(table_name, remaining_data)

    return {"ids": deleted_ids, "count": len(deleted_ids)}


@handle_db_errors
def get_table_info(
    metadata: Dict[str, Any],
    table_name: str,
) -> Dict[str, Any]:
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не найдена")

    data = load_table_data(table_name)
    table_info = metadata[table_name].copy()
    table_info["name"] = table_name
    table_info["record_count"] = len(data)

    return table_info
