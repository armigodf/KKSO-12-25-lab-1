import os
import struct
import sys


def sozdat_archiv(archiv_name, folder_line):
    with open(archiv_name, "wb") as archiv:  # Открывает или записывает файл в бинарном виде
        for i in os.listdir(folder_line):  # Формирую полный путь к объекту
            file_line = os.path.join(folder_line, i)
            if os.path.isfile(file_line):
                dob_file_v_archive(archiv, file_line, i)
    print(f"Архив {archiv_name} создан")


def dob_file_v_archive(archive_file, file_line, filename):
    name_v_bytax = filename.encode('utf-8')
    with open(file_line, "rb") as f:  # Открываем исходный файл для чтения в бинарном режиме
        soderzhimoe = f.read()

    # Запись длины имени, Имени, Размер содержимого и само содержимое
    archive_file.write(struct.pack('I', len(name_v_bytax)))
    archive_file.write(name_v_bytax)
    archive_file.write(struct.pack('Q', len(soderzhimoe)))
    archive_file.write(soderzhimoe)


def raspakoyka_archive(archive_name, folder_mesto):  # Если папки для распакоуки нет, создаем её
    if not os.path.exists(folder_mesto):
        os.makedirs(folder_mesto)

    with open(archive_name, "rb") as archive:
        while True:
            data = archive.read(4)  # читаем первые 4 быйта(там длинна имени следующего файла)
            if not data:
                break
            len_name = struct.unpack("I", data)[0]
            filename = archive.read(len_name).decode('utf-8')

            size_data = archive.read(8)
            if not size_data:
                break
            len_soderzhimoe = struct.unpack('Q', size_data)[0]
            soderzhimoe = archive.read(len_soderzhimoe)

            with open(os.path.join(folder_mesto, filename), "wb") as f:  # создаю файл в папке назначения и записываю в него данные
                f.write(soderzhimoe)
    print(f"Архив распакован в {folder_mesto}")


def add_v_archive(archive_name, file_line):
    filename = os.path.basename(file_line)
    with open(archive_name,
              "ab") as archive:  # Открываю существующий архив в режиме append binary для дозаписи в конец
        dob_file_v_archive(archive, file_line, filename)
    print(f"Файл {filename} добавлен в архив")


def remove_iz_archive(archive_name, remove_file):
    fix_file = os.path.basename(remove_file)
    tmp_archive = archive_name + ".tmp"
    found = False
    # Cтарый архив для чтения, а новый для записи
    with open(archive_name, "rb") as old_archive, open(tmp_archive, "wb") as new_archive:
        while True:
            data = old_archive.read(4)
            if not data:
                break

            len_name = struct.unpack("I", data)[0]
            name_file = old_archive.read(len_name).decode('utf-8')
            len_soderzhimoe = struct.unpack('Q', old_archive.read(8))[0]

            if name_file == fix_file:
                old_archive.seek(len_soderzhimoe, 1)
                found = True
            else:
                new_archive.write(struct.pack('I', len_name))
                new_archive.write(name_file.encode('utf-8'))
                new_archive.write(struct.pack('Q', len_soderzhimoe))
                new_archive.write(old_archive.read(len_soderzhimoe))

    os.replace(tmp_archive, archive_name)
    print(f"Файл {fix_file} {'удален' if found else 'не найден'}")


def main():
    if len(sys.argv) < 4:
        print("Использование: python archiver.py <command> <archive> <path>")
        return

    cmd = sys.argv[1]
    arc = sys.argv[2]
    path = sys.argv[3]

    if cmd == "create":
        sozdat_archiv(arc, path)
    elif cmd == "unpack":
        raspakoyka_archive(arc, path)
    elif cmd == "add":
        add_v_archive(arc, path)
    elif cmd == "remove":
        remove_iz_archive(arc, path)


if __name__ == "__main__":
    main()
