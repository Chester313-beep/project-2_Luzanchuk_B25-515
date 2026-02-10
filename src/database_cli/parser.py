import re
from typing import Dict, List, Optional, Tuple
class CommandParser:
    @staticmethod
    def parse_insert(command: str) -> Tuple[str, List[str]]:
        pattern = r'insert\s+(\w+)\s+values\s*\((.*)\)'
        match = re.match(pattern, command, re.IGNORECASE)
        if not match:
            raise ValueError("Неверный формат команды INSERT")
        table_name = match.group(1)
        values_str = match.group(2)
        values = []
        current = ""
        in_quotes = False
        quote_char = None
        for char in values_str:
            if char in ['"', "'"]:
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    if current and current[-1] != '\\':
                        in_quotes = False
                current += char
            elif char == ',' and not in_quotes:
                values.append(current.strip())
                current = ""
            else:
                current += char
        if current:
            values.append(current.strip())
        cleaned = []
        for v in values:
            v = v.strip()
            if (v.startswith('"') and v.endswith('"')) or \
               (v.startswith("'") and v.endswith("'")):
                v = v[1:-1]
            cleaned.append(v)
        return table_name, cleaned
    @staticmethod
    def parse_select(command: str) -> Tuple[str, Optional[Dict[str, str]]]:
        if 'where' in command.lower():
            pattern = r'select\s+(\w+)\s+where\s+(.+)'
            match = re.match(pattern, command, re.IGNORECASE)
            if not match:
                raise ValueError("Неверный формат команды SELECT")
            table_name = match.group(1)
            where_str = match.group(2)
            if '=' in where_str:
                col, val = where_str.split('=', 1)
                col = col.strip()
                val = val.strip()
                if (val.startswith('"') and val.endswith('"')) or \
                   (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                return table_name, {col: val}
            else:
                raise ValueError("Неверный формат условия WHERE. Используйте: where <столбец> = <значение>")
        else:
            pattern = r'select\s+(\w+)'
            match = re.match(pattern, command, re.IGNORECASE)
            if not match:
                raise ValueError("Неверный формат команды SELECT")
            table_name = match.group(1)
            return table_name, None
    @staticmethod
    def parse_update(command: str) -> Tuple[str, Dict[str, str], Dict[str, str]]:
        pattern = r'update\s+(\w+)\s+(.+?)\s+where\s+(.+)'
        match = re.match(pattern, command, re.IGNORECASE)
        if not match:
            raise ValueError("Неверный формат команды UPDATE")
        table_name = match.group(1)
        set_str = match.group(2)
        where_str = match.group(3)
        set_clause = {}
        if '=' in set_str:
            col, val = set_str.split('=', 1)
            col = col.strip()
            val = val.strip()
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            set_clause[col] = val
        where_clause = {}
        if '=' in where_str:
            col, val = where_str.split('=', 1)
            col = col.strip()
            val = val.strip()
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            where_clause[col] = val
        return table_name, set_clause, where_clause
    @staticmethod
    def parse_delete(command: str) -> Tuple[str, Dict[str, str]]:
        """Парсит команду DELETE"""
        pattern = r'delete\s+(\w+)\s+where\s+(.+)'
        match = re.match(pattern, command, re.IGNORECASE)
        if not match:
            raise ValueError("Неверный формат команды DELETE")
        table_name = match.group(1)
        where_str = match.group(2)
        where_clause = {}
        if '=' in where_str:
            col, val = where_str.split('=', 1)
            col = col.strip()
            val = val.strip()
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            where_clause[col] = val
        return table_name, where_clause
    @staticmethod
    def parse_info(command: str) -> str:
        pattern = r'info\s+(\w+)'
        match = re.match(pattern, command, re.IGNORECASE)
        if not match:
            raise ValueError("Неверный формат команды INFO")
        return match.group(1)