import json
from pathlib import Path
from typing import Any, Dict, List


def load_metadata() -> Dict[str, Any]:
    metadata_file = Path("data") / "metadata.json"

    if metadata_file.exists():
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data is None:
                    return {}
                return data
        except (json.JSONDecodeError, IOError):
            return {}

    return {}


def save_metadata(metadata: Dict[str, Any]) -> None:
    if metadata is None:
        raise ValueError("Нельзя сохранять None в качестве метаданных")

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    metadata_file = data_dir / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def load_table_data(table_name: str) -> List[Dict[str, Any]]:
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    data_file = data_dir / f"{table_name}.json"
    if data_file.exists():
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    return []


def save_table_data(table_name: str, data: List[Dict[str, Any]]) -> None:
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    data_file = data_dir / f"{table_name}.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def convert_to_type(value: str, target_type: str) -> Any:
    target_type = target_type.lower()

    if target_type == "int":
        return int(value)
    elif target_type == "float":
        return float(value)
    elif target_type == "bool":
        return value.lower() in ("true", "1", "yes", "да")
    elif target_type == "str":
        return str(value).strip("'\"")
    else:
        raise ValueError(f"Неизвестный тип: {target_type}")


def validate_data_type(value: str, expected_type: str) -> bool:
    try:
        convert_to_type(value, expected_type)
        return True
    except ValueError:
        return False
