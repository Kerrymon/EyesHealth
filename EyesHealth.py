import sys
import numpy as np
import cv2 as cv
import tkinter as tk
from tkinter import ttk
from tkinter import *
import requests
import telegram


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

def sendandclose():
    bot = telegram.Bot('1800511746:AAFW0CUXSEaiFsxSUgYhWqOQ8fwTJeehpnU')

    bot.send_video(chat_id='-1001523285912', video=open('output.avi', 'rb'), timeout=1000000)

    sys.exit()


if __name__ == "__main__":


    root = Tk()
    root.title("EyesHealth")
    root.geometry("150x110")
    root.resizable(width=False,height=False)
    start_button = tk.Button(root, text="Start", command=saving_video, height=3, width=20).grid(column=0, row=0)
    stop_button = tk.Button(root, text="Send and close", command=sendandclose, height=3, width=20).grid(column=0, row=1)

    root.mainloop()



