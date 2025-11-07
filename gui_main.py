from gui.file_explorer import setFilePath
from tkinter import *

def selectPath():
    path.set(setFilePath())

win = Tk()

win.title("File-Integrity-Checker")
win.geometry("600x300")
win.resizable(False, False)

name = Label(win, text = "File-Integrity-Checker", font = "맑은고딕 25")
name.place(x = 150, y = 10)

path = StringVar()

filePath = Entry(win, textvariable = path, width = 55, relief = "flat", font = "맑은고딕 10", state = "readonly")
filePath.place(x = 170, y = 72)

pathSelectionButton = Button(win, text = "경로 선택", width = 10, height = 2, overrelief = "flat", font = "맑은고딕 10", command = selectPath)
pathSelectionButton.place(x = 50, y = 60)

scanButton = Button(win, text = "최초 스캔", width = 10, height = 2, overrelief = "flat", font = "맑은고딕 10")
scanButton.place(x = 50, y = 130)

checkButton = Button(win, text = "무결성 검사", width = 10, height = 2, overrelief = "flat", font = "맑은고딕 10")
checkButton.place(x = 50, y = 200)

win.mainloop()