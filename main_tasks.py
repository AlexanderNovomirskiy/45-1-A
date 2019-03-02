from модули.xdb_to_ram import xdb_to_ram
from модули.ram_to_xdb import ram_to_xdb
from модули.ram_to_dbd import ram_to_dbd
from модули.dbd_to_ram import dbd_to_ram
import argparse  # Загружаем библиотеку обработки параметров консоли
import os.path  # Загружаем модуль для работы с путями


if __name__ == "__main__":
    #
    # Преобразование XDB -> RAM -> DBD -> RAM -> XDB1
    #
    file = 'материалы/tasks.xdb'
    description = 'Программа преобразования данных файла "%s".' % file
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-f', '--file', default=file,
                        help='Преобразование XDB -> RAM -> DBD.'
                        )

    args_xdb = parser.parse_args()
    args_dbd = parser.parse_args()
    args_dbd.file = args_dbd.file.replace('.xdb', '.db')
    print("%s\n" % parser.description)

    if not os.path.exists(args_xdb.file):
        raise FileNotFoundError("Файла %s не существует." % args_xdb.file)

    xram = xdb_to_ram(args_xdb.file)
    xram.parsing()
    print("Преобразование XDB -> RAM завершено!")
    
    if os.path.exists(args_dbd.file):
        raise FileExistsError("Файл %s уже существует." % args_dbd.file)

    dbd = ram_to_dbd(args_dbd.file, xram.schema)
    dbd.parsing()
    print("Преобразование RAM -> DBD завершено!")

    dram = dbd_to_ram(args_dbd.file)
    dram.parsing()
    print("Преобразование DBD -> RAM завершено!")

    xbd = ram_to_xdb(args_xdb.file.replace('.xdb', '1.xdb'), dram.schema)
    xbd.parsing()
    print("Преобразование RAM -> XBD завершено!")
    print("\nПреобразование XDB ->  DBD -> XDB1 завершено!")

    # Сравнение XDB и XDB1
    xdb = args_xdb.file  # Путь к исходному файлу
    xdb1 = args_xdb.file.replace('.xdb', '1.xdb')  # Путь к получившемуся файлу

    # Разбиваем файлы на два множества
    data = [set(open(i, encoding='utf-8').read().split()) for i in (xdb, xdb1)]
    diff = data[0].difference(data[1])  # Получаем все различия в файлах
    if diff:  # Если они есть
        print('\nМежду XDB и XDB1 есть различия!')
    else:
        print('\nМежду XDB и XDB1 нет различий!')
