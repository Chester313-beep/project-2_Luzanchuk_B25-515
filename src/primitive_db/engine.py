def welcome():
    print("Первая попытка запустить проект!")
    print("***")
    while True:
        print("<command> exit - выйти из программы")
        print("<command> help - справочная информация")
        command = input("Введите команду: ").strip().lower()
        if command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        elif command == "exit":
            print("Выход из программы.")
            break
        else:
            print(f"Неизвестная команда: '{command}'")
            print("Доступные команды: help, exit")