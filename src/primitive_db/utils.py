import json
import os
from typing import Any, Dict


def load_metadata(filepath: str) -> Dict[str, Any]:


    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка: файл {filepath} поврежден или имеет неверный формат JSON")
        return {}


def save_metadata(filepath: str, data: Dict[str, Any]) -> None:
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Метаданные успешно сохранены в {filepath}")
    except (IOError, OSError) as e:
        print(f"Ошибка при сохранении файла {filepath}: {e}")
        raise