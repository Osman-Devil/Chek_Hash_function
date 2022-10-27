import hashlib
import os
import json
from tkinter import filedialog, scrolledtext
import tkinter
from tkinter import *
import time


def scan_sha256(file):
    virus_found = False

    with open(file, "rb") as f:
        bytes = f.read()
        readable_hash = hashlib.sha256(bytes).hexdigest()

        print("The SHA256 hash of this file is: " + readable_hash)

        with open("SHA256.txt", 'r') as f:
            lines = [line.rstrip() for line in f]
            for line in lines:
                if str(readable_hash) == str(line.split(";")[0]):
                    virus_found = True

            f.close()

    if not virus_found:
        print("File is safe!")
        label_status.configure(text="Status: File is safe!", width=100, height=4,
                               fg="blue")
    else:
        print("Virus detected! File quarentined")
        label_status.configure(text="Status: Virus detected! File Deleted!", width=100, height=4,
                               fg="blue")
        os.remove(file)


def scan_md5(file):
    virus_found = False

    with open(file, "rb") as f:
        bytes = f.read()
        readable_hash = hashlib.md5(bytes).hexdigest()

        print("The MD5 hash of this file is: " + readable_hash)

        with open("MD5 Virus Hashes.txt", 'r') as f:
            lines = [line.rstrip() for line in f]
            for line in lines:
                if str(readable_hash) == str(line.split(";")[0]):
                    virus_found = True

            f.close()

    if not virus_found:
        print("File is safe!")
        label_status.configure(text="Status: File is safe!", width=100, height=4,
                               fg="blue")

        scan_sha256(file)
    else:
        print("Virus detected! File quarentined")
        label_status.configure(text="Status: Virus detected! File Deleted!", width=100, height=4,
                               fg="blue")
        os.remove(file)


def scan(file):
    virus_found = False

    with open(file, "rb") as f:
        bytes = f.read()
        readable_hash = hashlib.sha1(bytes).hexdigest()

        print("The SHA1 hash of this file is: " + readable_hash)

        with open('SHA1 HASHES.json', 'r') as f:
            dataset = json.loads(f.read())

            for index, item in enumerate(dataset["data"]):
                if str(item['hash']) == str(readable_hash):
                    virus_found = True

            f.close()

    if not virus_found:
        print("File is safe!")
        label_status.configure(text="Status: File is safe!", width=100, height=4,
                               fg="blue")

        scan_md5(file)
    else:
        print("Virus detected! File quarantined")
        label_status.configure(text="Status: Virus detected! File Deleted!", width=100, height=4,
                               fg="blue")
        os.remove(file)


def browse_button():
    filename = filedialog.askdirectory()
    files = os.listdir(filename)
    opened_file.configure(text="Открыта папка: " + filename)
    a = files
    for i in range(len(a)):
        txt.insert(INSERT, filename + "/" + a[i] + "\n")
        b = filename + "/" + a[i]
        scan(b)


def write():
    a = txt.get('1.0', 'end-1c')
    fl = open("output.txt", "w")
    fl.write(a)


def timer():
    start_time = time.time()
    # print("tick")
    while True:
        with open("output.txt", "r") as f:
            for line in f:
                # print(line.rstrip("\n"))
                scan(line.rstrip("\n"))
            time.sleep(10.0 - ((time.time() - start_time) % 10.0))
            # if button_2 == True:
            #     start_time.stop()
        window.update()


def browseFiles():
    filename1 = filedialog.askopenfilename(initialdir="/",
                                           title="Select a File",
                                           filetypes=(("Text files",
                                                       "*.*"),
                                                      ("all files",
                                                       "*.*")))

    opened_file.configure(text="Открыт файл: " + filename1)

    scan(filename1)


window = tkinter.Tk()

window.iconbitmap(r'G:\Питон 3.0\gratis-png-icono-de-ico-fantasma-thumbnail.ico')

window.title('Antivirus')

window.geometry("500x500")

window.config(background="#ff8000")

label_status = Label(window,
                     text="Статус: ",
                     width=100, height=4,
                     fg="black",
                     bg="#ff8000")

label_status.config(font=("Courier", 10))

opened_file = Label(window,
                    text="Открыт файл: ",
                    width=100, height=4,
                    fg="black",
                    bg="#ff8000")

opened_file.config(font=("Courier", 10))

txt = scrolledtext.ScrolledText(window, width=52, height=20)
txt.pack()
txt.place(x=30, y=50)

button_1 = Button(window, text="Запись", command=write)
button_1.grid(row=2, column=1)
button_1.place(x=424, y=430)

# button_2 = Button(window, text="Стоп", command=write)
# button_2.grid(row=2, column=1)
# button_2.place(x=370, y=430)

button_3 = Button(window, text="Проверка через 10 секунд", command=timer)
button_3.grid(row=2, column=1)
button_3.place(x=320, y=460)

folder_path = StringVar()
button4 = Button(window, text="Загрузить папку", command=browse_button)
button4.grid(row=2, column=1)
button4.place(x=120, y=460)

button_explore = Button(window,
                        text="Загрузить файл",
                        command=browseFiles)

opened_file.grid(column=1, row=1)
opened_file.place(x=-150, y=360)

label_status.grid(column=1, row=1)
label_status.place(x=-150, y=400)

button_explore.grid(column=1, row=2)
button_explore.place(x=10, y=460)

btn = Button(window, text='Очистить', command=lambda: txt.delete(1.0, END))
btn.pack()
btn.grid(column=4, row=4)
btn.place(x=235, y=460)

window.mainloop()

