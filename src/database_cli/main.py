#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from engine import display_welcome, execute_command
    from utils import load_metadata
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    sys.exit(1)


def main():
    display_welcome()
    os.makedirs("data", exist_ok=True)

    metadata = load_metadata()

    while True:
        try:
            command = input("\nВведите команду (help для справки): ").strip()
            if not command:
                continue

            if not execute_command(command, metadata):
                break

            metadata = load_metadata()
        except KeyboardInterrupt:
            print("\n\nПрограмма завершена.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
