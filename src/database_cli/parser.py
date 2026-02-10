import re
from typing import Any, Dict, List, Optional, Tuple


def parse_create(command: str) -> Tuple[str, List[str]]:
    pattern = r'create\s+(\w+)\s*\((.*)\)'
    match = re.match(pattern, command, re.IGNORECASE)

    if not match:
        raise ValueError("Неверный формат команды CREATE")
    table_name = match.group(1)
    columns_str = match.group(2).strip()
    columns_raw = [col.strip() for col in columns_str.split(',')]
    columns = []
    for col in columns_raw:
        if col and ' ' not in col:
            col = col + ' str'
        columns.append(col)
    return table_name, columns


def parse_drop(command: str) -> str:
    pattern = r'drop\s+(\w+)'
    match = re.match(pattern, command, re.IGNORECASE)

    if not match:
        raise ValueError("Неверный формат команды DROP")

    return match.group(1)


def parse_insert(command: str) -> Tuple[str, List[str]]:
    pattern = r'insert\s+(\w+)\s+values\s*\((.*)\)'
    match = re.match(pattern, command, re.IGNORECASE)

    if not match:
        raise ValueError("Неверный формат команды INSERT")

    table_name = match.group(1)
    values_str = match.group(2).strip()
    values = [val.strip() for val in values_str.split(',')]

    return table_name, values


def parse_select(command: str) -> Tuple[str, Optional[Dict[str, Any]]]:
    where_pattern = r'select\s+(\w+)\s+where\s+(.+)=(.+)'
    match = re.match(where_pattern, command, re.IGNORECASE)

    if match:
        table_name = match.group(1).strip()
        column = match.group(2).strip()
        value = match.group(3).strip()
        return table_name, {column: value}
    else:
        pattern = r'select\s+(\w+)'
        match = re.match(pattern, command, re.IGNORECASE)

        if not match:
            raise ValueError("Неверный формат команды SELECT")

        return match.group(1), None


def parse_update(command: str) -> Tuple[str, Dict[str, Any], Dict[str, Any]]:
    pattern = r'update\s+(\w+)\s+set\s+(.+)\s+where\s+(.+)=(.+)'
    match = re.match(pattern, command, re.IGNORECASE)

    if not match:
        raise ValueError(
            "Неверный формат условия WHERE. "
            "Используйте: where <столбец> = <значение>"
        )

    table_name = match.group(1).strip()
    set_clause_str = match.group(2).strip()
    where_column = match.group(3).strip()
    where_value = match.group(4).strip()

    set_clause = {}
    set_parts = set_clause_str.split(',')
    for part in set_parts:
        key_value = part.split('=')
        if len(key_value) == 2:
            set_clause[key_value[0].strip()] = key_value[1].strip()

    where_clause = {where_column: where_value}

    return table_name, set_clause, where_clause


def parse_delete(command: str) -> Tuple[str, Dict[str, Any]]:
    pattern = r'delete\s+(\w+)\s+where\s+(.+)=(.+)'
    match = re.match(pattern, command, re.IGNORECASE)

    if not match:
        raise ValueError("Неверный формат команды DELETE")

    table_name = match.group(1).strip()
    column = match.group(2).strip()
    value = match.group(3).strip()

    return table_name, {column: value}


def parse_info(command: str) -> str:
    pattern = r'info\s+(\w+)'
    match = re.match(pattern, command, re.IGNORECASE)

    if not match:
        raise ValueError("Неверный формат команды INFO")

    return match.group(1)
COMMAND_PARSERS = {
    'create': parse_create,
    'drop': parse_drop,
    'insert': parse_insert,
    'select': parse_select,
    'update': parse_update,
    'delete': parse_delete,
    'info': parse_info,
}
