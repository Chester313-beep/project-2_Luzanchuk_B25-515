#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from engine import display_welcome, execute_command
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что engine.py находится в той же директории")
    sys.exit(1)

def main():
    display_welcome()
    os.makedirs("data", exist_ok=True)
    
    while True:
        try:
            command = input("\n>>> Введите команду: ").strip()
            if not command:
                continue
            if execute_command(command):
                break
        except KeyboardInterrupt:
            print("\n\nВыход из программы...")
            break
        except EOFError:
            print("\n\nПрограмма завершена.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")
if __name__ == "__main__":
    main()