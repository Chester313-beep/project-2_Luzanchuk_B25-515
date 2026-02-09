import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from engine import welcome
except ImportError:
    try:
        from engine import welcome
    except ImportError:
        print("Ошибка: не могу импортировать engine")
        sys.exit(1)
def main() -> int:
    welcome()
    return 0


if __name__ == "__main__":
    sys.exit(main())