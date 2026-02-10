import re
from typing import Any, Dict, List, Optional

try:
    from .utils import load_table_data, save_table_data, convert_to_type, validate_data_type
except ImportError:
    from utils import load_table_data, save_table_data, convert_to_type, validate_data_type


def create_table(
    metadata: Dict[str, Any], 
    table_name: str, 
    columns: List[str]
) -> Dict[str, Any]:
    if not table_name or not table_name.strip():
        raise ValueError("Имя таблицы не может быть пустым")
    table_name = table_name.strip()
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
        raise ValueError(
            f"Имя таблицы '{table_name}' содержит недопустимые символы. "
            "Допустимы только буквы, цифры и подчеркивание"
        )
    if table_name in metadata:
        raise ValueError(f"Таблица '{table_name}' уже существует")
    columns_dict = {"ID": "int"}
    for i, column in enumerate(columns):
        if ':' not in column:
            raise ValueError(
                f"Столбец '{column}' имеет неверный формат. "
                "Используйте формат 'имя:тип' (например, 'name:str')"
            )
        col_name, col_type = column.split(':', 1)
        col_name = col_name.strip()
        col_type = col_type.strip().lower()
        if not col_name:
            raise ValueError(f"Имя столбца не может быть пустым (столбец #{i})")
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', col_name):
            raise ValueError(
                f"Имя столбца '{col_name}' содержит недопустимые символы"
            )
        if col_type not in ('int', 'str', 'bool', 'float'):
            raise ValueError(
                f"Недопустимый тип данных '{col_type}' для столбца '{col_name}'. "
                "Допустимые типы: int, str, bool, float"
            )
        columns_dict[col_name] = col_type
    metadata[table_name] = {
        "columns": columns_dict,
        "primary_key": "ID"
    }
    save_table_data(table_name, [])
    return metadata
def drop_table(metadata: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    """Удаляет таблицу"""
    table_name = table_name.strip()
    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не существует")
    del metadata[table_name]
    return metadata
def list_tables(metadata: Dict[str, Any]) -> List[str]:
    return list(metadata.keys())
def describe_table(
    metadata: Dict[str, Any], 
    table_name: str
) -> Optional[Dict[str, Any]]:
    table_name = table_name.strip()
    return metadata.get(table_name)
def insert(
    metadata: Dict[str, Any], 
    table_name: str, 
    values: List[str]
) -> Dict[str, Any]:
    table_name = table_name.strip()
    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не существует")
    schema = metadata[table_name]["columns"]
    column_names = list(schema.keys())
    expected_count = len(column_names) - 1
    if len(values) != expected_count:
        raise ValueError(
            f"Неверное количество значений. Ожидается {expected_count}, получено {len(values)}"
        )
    data = load_table_data(table_name)
    new_id = 1
    if data:
        ids = [record.get("ID", 0) for record in data]
        new_id = max(ids) + 1 if ids else 1
    new_record = {"ID": new_id}
    for i, col_name in enumerate(column_names[1:], 0):  # Пропускаем ID
        col_type = schema[col_name]
        value_str = values[i]
        try:
            converted_value = convert_to_type(value_str, col_type)
            if not validate_data_type(converted_value, col_type):
                raise ValueError(f"Неверный тип для столбца '{col_name}'")
            new_record[col_name] = converted_value
        except Exception as e:
            raise ValueError(f"Ошибка в столбце '{col_name}': {e}")
    data.append(new_record)
    save_table_data(table_name, data)
    return {"id": new_id, "table_name": table_name, "data": data}
def select(
    metadata: Dict[str, Any],
    table_name: str,
    where_clause: Optional[Dict[str, str]] = None
) -> List[Dict[str, Any]]:
    table_name = table_name.strip()
    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не существует")
    data = load_table_data(table_name)
    if not data or where_clause is None:
        return data
    schema = metadata[table_name]["columns"]
    result = []
    for record in data:
        match = True
        for column, value in where_clause.items():
            if column not in record:
                match = False
                break
            col_type = schema.get(column, "str")
            try:
                converted_value = convert_to_type(value, col_type)
                if str(record[column]) != str(converted_value):
                    match = False
                    break
            except:
                match = False
                break
        if match:
            result.append(record)
    return result
def update(
    metadata: Dict[str, Any],
    table_name: str,
    set_clause: Dict[str, str],
    where_clause: Dict[str, str]
) -> Dict[str, Any]:
    table_name = table_name.strip()
    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не существует")
    data = load_table_data(table_name)
    if not data:
        return {"count": 0, "ids": [], "data": data}
    schema = metadata[table_name]["columns"]
    updated_ids = []
    for record in data:
        match = True
        for column, value in where_clause.items():
            if column not in record:
                match = False
                break
            col_type = schema.get(column, "str")
            try:
                converted_value = convert_to_type(value, col_type)
                if str(record[column]) != str(converted_value):
                    match = False
                    break
            except:
                match = False
                break
        if match:
            for column, new_value in set_clause.items():
                if column in schema and column != "ID":
                    col_type = schema[column]
                    try:
                        converted_value = convert_to_type(new_value, col_type)
                        record[column] = converted_value
                    except Exception as e:
                        raise ValueError(f"Ошибка обновления '{column}': {e}")
            updated_ids.append(record["ID"])
    if updated_ids:
        save_table_data(table_name, data)
    return {"count": len(updated_ids), "ids": updated_ids, "data": data}
def delete(
    metadata: Dict[str, Any],
    table_name: str,
    where_clause: Dict[str, str]
) -> Dict[str, Any]:
    table_name = table_name.strip()
    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не существует")
    data = load_table_data(table_name)
    if not data:
        return {"count": 0, "ids": [], "data": data}
    schema = metadata[table_name]["columns"]
    new_data = []
    deleted_ids = []
    for record in data:
        match = True
        for column, value in where_clause.items():
            if column not in record:
                match = False
                break
            col_type = schema.get(column, "str")
            try:
                converted_value = convert_to_type(value, col_type)
                if str(record[column]) != str(converted_value):
                    match = False
                    break
            except:
                match = False
                break
        if match:
            deleted_ids.append(record["ID"])
        else:
            new_data.append(record)
    if deleted_ids:
        save_table_data(table_name, new_data)
    return {"count": len(deleted_ids), "ids": deleted_ids, "data": new_data}
def get_table_info(
    metadata: Dict[str, Any],
    table_name: str
) -> Dict[str, Any]:
    table_name = table_name.strip()
    if table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не существует")
    data = load_table_data(table_name)
    table_info = metadata[table_name].copy()
    table_info["name"] = table_name
    table_info["record_count"] = len(data)
    return table_info