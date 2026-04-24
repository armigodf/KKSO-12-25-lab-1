import os


def sozdat_archiv(archiv_name, folder_line):
    with open(archiv_name, "wb") as archiv:  # Открывает или записывает файл в бинарном виде
        for i in os.listdir(folder_line):
            file_line = os.path.join(folder_line, i)
            if os.path.isfile(file_line):
                name_v_bytax = i.encode('utf_8')
                with open(file_line, "rb") as f:
                    soderzhimoe = f.read()
