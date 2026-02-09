import re
from typing import Any, Dict, List, Optional


def create_table(
    metadata: Dict[str, Any], 
    table_name: str, 
    columns: List[str]
) -> Dict[str, Any]:
    if not table_name or not table_name.strip():
        raise ValueError("Имя таблицы не может быть пустым")
    table_name = table_name.strip()
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
        error_msg = (
            f"Имя таблицы '{table_name}' содержит недопустимые символы. "
            "Допустимы только буквы, цифры и подчеркивание, "
            "начиная с буквы или подчеркивания."
        )
        raise ValueError(error_msg)
    if table_name in metadata:
        raise ValueError(f"Таблица '{table_name}' уже существует")
    columns_with_id = ["ID:int"] + columns
    validated_columns = []
    for i, column in enumerate(columns_with_id):
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
            error_msg = (
                f"Имя столбца '{col_name}' содержит недопустимые символы. "
                "Допустимы только буквы, цифры и подчеркивание, "
                "начиная с буквы или подчеркивания."
            )
            raise ValueError(error_msg)
        if col_type not in ('int', 'str', 'bool'):
            raise ValueError(
                f"Недопустимый тип данных '{col_type}' для столбца '{col_name}'. "
                "Допустимые типы: int, str, bool"
            )
        validated_columns.append(f"{col_name}:{col_type}")
    metadata[table_name] = {
        "columns": validated_columns,
        "primary_key": "ID",
        "row_count": 0,
        "created_at": "текущая_дата"
    }
    return metadata
def drop_table(metadata: Dict[str, Any], table_name: str) -> Dict[str, Any]:
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