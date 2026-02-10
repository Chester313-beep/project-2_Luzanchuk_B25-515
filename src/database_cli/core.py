import json
import os
from typing import Any, Dict, List, Optional

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

from src.decorators import confirm_action, create_cacher, handle_db_errors, log_time

cache_result = create_cacher()


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.tables = {}

    @handle_db_errors
    def create_table(self, table_name, columns):
        if table_name in self.tables:
            raise ValueError(f"Таблица {table_name} уже существует")

        self.tables[table_name] = {
            'columns': columns,
            'data': [],
            'next_id': 1,
        }
        print(f"Таблица '{table_name}' создана")

    @confirm_action("удаление таблицы")
    @handle_db_errors
    def drop_table(self, table_name):
        if table_name not in self.tables:
            raise KeyError(f"Таблица {table_name} не найдена")

        del self.tables[table_name]
        print(f"Таблица '{table_name}' удалена")

    @log_time
    @handle_db_errors
    def select(self, table_name, condition=None, columns=None):
        cache_key = f"select_{table_name}_{str(condition)}_{str(columns)}"

        return cache_result(
            cache_key,
            lambda: self._execute_select(table_name, condition, columns),
        )

    def _execute_select(self, table_name, condition=None, columns=None):
        if table_name not in self.tables:
            raise KeyError(f"Таблица {table_name} не найдена")

        table = self.tables[table_name]
        result = []

        for row in table['data']:
            if condition is None or condition(row):
                if columns is None:
                    result.append(row.copy())
                else:
                    filtered_row = {col: row[col] for col in columns if col in row}
                    result.append(filtered_row)

        return result

    @log_time
    @handle_db_errors
    def insert(self, table_name, data):
        if table_name not in self.tables:
            raise KeyError(f"Таблица {table_name} не найдена")

        table = self.tables[table_name]

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
    def delete(self, table_name, condition):
        if table_name not in self.tables:
            raise KeyError(f"Таблица {table_name} не найдена")

        table = self.tables[table_name]
        initial_count = len(table['data'])

        table['data'] = [row for row in table['data'] if not condition(row)]

        deleted_count = initial_count - len(table['data'])
        print(f"Удалено {deleted_count} записей из таблицы '{table_name}'")
        return deleted_count

    @handle_db_errors
    def update(self, table_name, condition, updates):
        if table_name not in self.tables:
            raise KeyError(f"Таблица {table_name} не найдена")

        table = self.tables[table_name]
        updated_count = 0

        for row in table['data']:
            if condition(row):
                row.update(updates)
                updated_count += 1

        print(f"Обновлено {updated_count} записей в таблице '{table_name}'")
        return updated_count

    @handle_db_errors
    def save_to_file(self, filename):
        serializable_tables = {}
        for table_name, table_data in self.tables.items():
            serializable_tables[table_name] = {
                'columns': table_data['columns'],
                'data': table_data['data'],
                'next_id': table_data['next_id'],
            }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_tables, f, indent=2, ensure_ascii=False)

        print(f"База данных сохранена в файл '{filename}'")

    @handle_db_errors
    def load_from_file(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден")

        with open(filename, 'r', encoding='utf-8') as f:
            serializable_tables = json.load(f)

        self.tables = serializable_tables
        print(f"База данных загружена из файла '{filename}'")


def create_table(
    metadata: Dict[str, Any],
    table_name: str,
    columns: List[str],
) -> Dict[str, Any]:
    if table_name in metadata:
        raise ValueError(f"Таблица '{table_name}' уже существует")

    metadata[table_name] = {"columns": columns}
    return metadata


def drop_table(metadata: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не найдена")

    del metadata[table_name]
    return metadata


def list_tables(metadata: Dict[str, Any]) -> List[str]:
    return list(metadata.keys())


def describe_table(
    metadata: Dict[str, Any],
    table_name: str,
) -> Optional[Dict[str, Any]]:
    return metadata.get(table_name)


def insert(
    metadata: Dict[str, Any],
    table_name: str,
    values: List[str],
) -> Dict[str, Any]:
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не найдена")

    table_info = metadata[table_name]
    expected_count = len(table_info["columns"])

    if len(values) != expected_count:
        raise ValueError(
            f"Неверное количество значений. Ожидается {expected_count}, "
            f"получено {len(values)}"
        )

    data = load_table_data(table_name)
    new_record = {}
    new_id = len(data) + 1

    for i, col_name in enumerate(table_info["columns"]):
        try:
            converted_value = convert_to_type(values[i], col_name.split(" ")[1])
            new_record[col_name] = converted_value
        except Exception as e:
            raise ValueError(f"Ошибка в столбце '{col_name}': {e}") from e

    data.append(new_record)
    save_table_data(table_name, data)

    return {"id": new_id}


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
                        col_type = col_def.split(" ")[1]
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
