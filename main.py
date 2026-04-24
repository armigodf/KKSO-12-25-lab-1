import os
import struct


def sozdat_archiv(archiv_name, folder_line):
    with open(archiv_name, "wb") as archiv:  # Открывает или записывает файл в бинарном виде
        for i in os.listdir(folder_line):
            file_line = os.path.join(folder_line, i)
            if os.path.isfile(file_line):
                name_v_bytax = i.encode('utf_8')
                with open(file_line, "rb") as f:
                    soderzhimoe = f.read()


def raspakoyka_archive(arcgive_name, folder_mesto):
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
