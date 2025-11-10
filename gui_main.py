from core_scan.scan import scanDirectoryToTxt, scanDirectoryToDict
from load_hashes.compare_hashes import compare_hashes
from gui.file_explorer import setFilePath
from tkinter import *
import os

class GuiApp:
    def __init__(self):
        self.win = Tk() #StringVar 변수 초기화 전 Tk()를 호출하여 Root Window 먼저 생성
        self.win.title("File-Integrity-Checker")
        self.win.geometry("600x300")
        self.win.resizable(False, False)

        self.path = StringVar()
        self.output_filePath = None
        self.firstScan_result = StringVar()

        self.setGui()
    
    def setGui(self):
        name = Label(self.win, text = "File-Integrity-Checker", font = "맑은고딕 25")
        name.place(x = 150, y = 10)

        filePath = Entry(self.win, textvariable = self.path, width = 55, relief = "flat", font = "맑은고딕 10", state = "readonly")
        filePath.place(x = 170, y = 86)

        firstScanResult = Entry(self.win, textvariable = self.firstScan_result, width = 55, relief = "flat", font = "맑은고딕 10", state = "readonly")
        firstScanResult.place(x = 170, y= 156)

        pathSelectionButton = Button(self.win, text = "경로 선택", width = 10, height = 2, overrelief = "flat", font = "맑은고딕 10", command = self.selectPath)
        pathSelectionButton.place(x = 50, y = 75)

        scanButton = Button(self.win, text = "최초 스캔", width = 10, height = 2, overrelief = "flat", font = "맑은고딕 10", command = self.firstScan)
        scanButton.place(x = 50, y = 145)

        checkButton = Button(self.win, text = "무결성 검사", width = 10, height = 2, overrelief = "flat", font = "맑은고딕 10")
        checkButton.place(x = 50, y = 215)

    def selectPath(self):
        self.path.set(setFilePath())
        self.output_filePath = os.path.join(self.path.get(), 'base_hash.txt')

    def firstScan(self):
        try:
            scan_results = scanDirectoryToTxt(self.path.get(), self.output_filePath)

            if scan_results:
                for item in scan_results:
                    if isinstance(item, tuple):
                        filePath, error = item

                        if error == "Permission Denied":
                            self.firstScan_result.set("스캔을 실패했습니다. 파일을 읽을 권한이 없습니다!")
                            break
                        elif error == "Error":
                            self.firstScan_result.set("스캔을 실패했습니다. 권한과 파일 경로 확인 후 다시 시도하세요!")
                            break
                    else:
                        continue
                
                self.firstScan_result.set(f"폴더 스캔을 완료했습니다.")
            else:
                self.firstScan_result.set("스캔을 실패했습니다. 권한과 파일 경로 확인 후 다시 시도하세요.")
        
        except FileNotFoundError:
            self.firstScan_result.set("스캔을 실패했습니다. 파일 경로를 재선택해주세요.")
        except PermissionError:
            self.firstScan_result.set("스캔을 실패했습니다. 파일을 읽을 권한이 없습니다!")
        except Exception as e:
            self.firstScan_result.set("스캔을 실패했습니다. 권한과 파일 경로 확인 후 다시 시도하세요!")

    def run(self):
        self.win.mainloop()

app = GuiApp()

app.run()