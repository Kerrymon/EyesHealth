import sys
import numpy as np
import cv2 as cv
import tkinter as tk
from tkinter import ttk
from tkinter import *
import requests
import telegram
from datetime import datetime, timedelta
from tkinter import messagebox
import time

def cam():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        color = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
        cv.imshow('frame', color)
        if cv.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv.destroyAllWindows()
            break

    cap.release()
    cv.destroyAllWindows()


def saving_video():
    cap = cv.VideoCapture(0)
    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = cv.flip(frame, 0)
        # write the flipped frame
        out.write(frame)
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    out.release()
    cv.destroyAllWindows()

def send():
    bot = telegram.Bot('1800511746:AAFW0CUXSEaiFsxSUgYhWqOQ8fwTJeehpnU')

    bot.send_message(chat_id='-1001523285912', text="User turned on pc and made gym for eyes in {}, 4 hours of learning left (in {} end)".format(datetime.now(), datetime.now() + timedelta(hours=3)))
    bot.send_video(chat_id='-1001523285912', video=open('output.avi', 'rb'), timeout=1000000)


def info_msg():
    info = Tk()
    info.title("Information")
    lbl_info = Label(info, text="1. Кнопка Start Eyegym включает запись с вебкамеры, записывая и сохраняя на компьютер видео.\n "
                                    "2. Кнопка Send Video отправляет запись с вебкамеры в закрытый телеграм канал, где находится только автор программы.\n"
                                    "3. Кнопка Start Button запускает/останавливает таймер, при каждом нажатии отправляется сообщение в закрытый телеграм канал.",  font=("Helvetica", 16, "bold"))
    lbl_info.pack()





def whole_seconds(time):
    return str(time).split('.')[0]


def update():
    if not pause_toggle.paused:
        timer.set(whole_seconds(datetime.now() - start_time - pause_timer.pause_time))
    else:
        this_pause = datetime.now() - pause_toggle.pause_start
        pause_timer.set(whole_seconds(this_pause + pause_timer.pause_time))
    root.after(100, update)


def pause_toggle():
    if pause_toggle.paused:
        pause_button['text'] = 'Pause'
        pause_timer.pause_time += datetime.now() - pause_toggle.pause_start
        seconds = int(pause_timer.get()[0])*3600 + int(pause_timer.get()[2]+pause_timer.get()[3])*60 + int(pause_timer.get()[5]+pause_timer.get()[6])
        time_remain = fourhours - seconds
        final_hours = 0
        final_minutes = 0
        final_seconds = 0
        while time_remain > 0:
            if time_remain >= 3600:
                final_hours += 1
                time_remain -= 3600
            elif time_remain >= 60:
                final_minutes += 1
                time_remain -= 60
            else:
                final_seconds += time_remain
                time_remain -= time_remain
        bot.send_message(chat_id='-1001523285912',
                         text="User started working... {} hour(s), {} minute(s), {} second(s) of time remaining...".format(final_hours, final_minutes, final_seconds))

    else:
        global number_of_pauses
        number_of_pauses += 1
        pause_button['text'] = 'Start'
        pause_toggle.pause_start = datetime.now()
        bot.send_message(chat_id='-1001523285912',
                         text="User stopped working... {} - time of pauses, {} - pauses have been made".format(pause_timer.get(), number_of_pauses))
    pause_toggle.paused = not pause_toggle.paused


def make_label(text):
    tk.Label(root, text=text, font=("Helvetica", 16)).pack()
    text_var = tk.StringVar()
    tk.Label(root, textvariable=text_var, font=("Helvetica", 16)).pack()
    return text_var


def on_closing():
    date_end = datetime.now()
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if timedelta(hours=4) - (date_end - date_start) < timedelta(0):
            bot.send_message(chat_id='-1001523285912',
                             text="User stopped working and finished the program... time is up, {} - time of pauses, {} - pauses have been made".format(pause_timer.get(), number_of_pauses))
        else:
            bot.send_message(chat_id='-1001523285912',
                             text="User stopped working and finished the program... {} of time remaining, {} - time of pauses, {} - pauses have been made".format(timedelta(hours=4) - (date_end - date_start),
                                 pause_timer.get(), number_of_pauses))
        root.destroy()





if __name__ == "__main__":
    bot = telegram.Bot('1800511746:AAFW0CUXSEaiFsxSUgYhWqOQ8fwTJeehpnU')

    date_start = datetime.now()

    root = Tk()
    root.title("EyesHealth")
    root.geometry("500x400")

    fourhours = 3600*4
    number_of_pauses = 0

    pause_toggle.paused = False

    timer, pause_timer = make_label("Work time"), make_label("Pause time")
    pause_button = tk.Button(root, text='Start pause', font=("Helvetica", 12, "bold"), command=pause_toggle)
    pause_button.pack(side=tk.BOTTOM, pady=10)

    pause_timer.pause_time = timedelta(0)
    pause_timer.set(whole_seconds(pause_timer.pause_time))
    start_time = datetime.now()
    update()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.resizable(width=False,height=False)
    start_button = tk.Button(root, text="Start Eyegym", command=saving_video, height=3, width=20).pack()
    stop_button = tk.Button(root, text="Send video", command=send, height=3, width=20).pack()
    info_button = tk.Button(root, text="Info", command=info_msg, height=3, width=20).pack()

    patch_v = tk.Label(root, text="patch 0.17", font=("Helvetica", 12, "bold"))
    patch_v.place(x=410, y=370)



    root.mainloop()



