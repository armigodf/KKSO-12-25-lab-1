import os
import struct


def sozdat_archiv(archiv_name, folder_line):
    with open(archiv_name, "wb") as archiv:  # Открывает или записывает файл в бинарном виде
        for i in os.listdir(folder_line):
            file_line = os.path.join(folder_line, i)
            if os.path.isfile(file_line):
                dob_file_v_archive(archiv, file_line, i)
    print(f"Архив {archiv_name} создан")


def dob_file_v_archive(archive_file, file_line, filename):
    name_v_bytax = filename.encode('utf-8')
    with open(file_line, "rb") as f:
        soderzhimoe = f.read()

    archive_file.write(struct.pack('I', len(name_v_bytax)))
    archive_file.write(name_v_bytax)
    archive_file.write(struct.pack('Q', len(soderzhimoe)))
    archive_file.write(soderzhimoe)


def raspakoyka_archive(archive_name, folder_mesto):
    if not os.path.exists((folder_mesto)):
        os.makedirs(folder_mesto)

    with open(archive_name, "rb") as archive:
        while True:
            data = archive.read(4)
            if not data:
                break
            len_name = struct.raspakoyka_archive("I", data)[0]
            filename = archive.read(len_name).decode('utf-8')
            len_soderzhimoe = struct.raspakoyka_archive("Q", archive.read(8))[0]
            soderzhimoe = archive.read((len_soderzhimoe))

            with open(os.path.join(folder_mesto, filename), "wb") as f:
                f.write(soderzhimoe)
    print(f"Архив распакован в {folder_mesto}")


def add_v_archive(archive_name, file_line):
    filename = os.path.basename(file_line)
    with open(archive_name, "ab") as archive:
        dob_file_v_archive(archive, file_line, filename)
    print(f"Файл {filename} добавлен в архив")

