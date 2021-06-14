import multiprocessing
import tkinter as tk
import cv2

e = multiprocessing.Event()


def startrecording(e):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc,  20.0, (640,480))

    while(cap.isOpened()):
        if e.is_set():
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            e.clear()
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
        else:
            break

def start_recording_proc():
    global p
    p = multiprocessing.Process(target=startrecording, args=(e,))
    p.start()


def stoprecording():
    e.set()
    p.join()

    root.quit()
    root.destroy()

#def output():


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("%dx%d+0+0" % (800, 600))
    startbutton=tk.Button(root,width=10,height=1,text='START',command=start_recording_proc)
    stopbutton=tk.Button(root,width=10,height=1,text='STOP', command=stoprecording)
    startbutton.pack()
    stopbutton.pack()
    root.mainloop()