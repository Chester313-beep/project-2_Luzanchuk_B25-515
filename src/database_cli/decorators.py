import functools
import time
from typing import Any, Callable, Dict


def handle_db_errors(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f"Ошибка: таблица или ключ не найдены - {e}")
            return None
        except ValueError as e:
            print(f"Ошибка валидации данных - {e}")
            return None
        except FileNotFoundError as e:
            print(f"Файл не найден - {e}")
            return None
        except Exception as e:
            print(f"Непредвиденная ошибка в функции {func.__name__} - {e}")
            return None

    return wrapper


def confirm_action(action_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            prompt = f'\nВы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            print(prompt, end='')
            response = input().strip().lower()

            if response != 'y':
                print("Операция отменена.")
                return None

            return func(*args, **kwargs)

        return wrapper
    return decorator


def log_time(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()

        elapsed = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд")

        return result

    return wrapper


def create_cacher() -> Callable:
    cache: Dict[str, Any] = {}

    def cache_result(key: str, value_func: Callable) -> Any:
        if key in cache:
            print(f"Используется кэшированный результат для ключа: {key}")
            return cache[key]

        result = value_func()
        cache[key] = result
        print(f"Результат закэширован с ключом: {key}")
        return result

    return cache_result
