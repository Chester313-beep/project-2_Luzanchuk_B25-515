#!/usr/bin/env python3
import sys

from primitive_db.engine import run


def main() -> int:
    """
    Точка входа в программу.
    Запускает основную функцию базы данных.
    """
    try:
        run()
        return 0
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена пользователем")
        return 130
    except Exception as e:
        print(f"Критическая ошибка: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())