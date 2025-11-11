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
        self.integrityCheck_result = StringVar()

        self.filePath = None
        self.firstScanResult = None
        self.integrityCheckResult = None

        self.setGui()
    
    def setGui(self):
        name = Label(self.win, text = "File-Integrity-Checker", font = "맑은고딕 25")
        name.place(x = 150, y = 10)

        self.filePath = Entry(self.win, textvariable = self.path, width = 55, relief = "flat", font = "맑은고딕 10", state = "readonly")
        self.filePath.place(x = 170, y = 86)

        self.firstScanResult = Entry(self.win, textvariable = self.firstScan_result, width = 55, relief = "flat", font = "맑은고딕 10", state = "readonly")
        self.firstScanResult.place(x = 170, y = 156)

        self.integrityCheckResult = Entry(self.win, textvariable = self.integrityCheck_result, width = 55, relief = "flat", font = "맑은고딕 10", state = "readonly")
        self.integrityCheckResult.place(x = 170, y = 226)

        pathSelectionButton = Button(self.win, text = "경로 선택", width = 10, height = 2, overrelief = "flat", font = "맑은고딕 10", command = self.selectPath)
        pathSelectionButton.place(x = 50, y = 75)

        scanButton = Button(self.win, text = "최초 스캔", width = 10, height = 2, overrelief = "flat", font = "맑은고딕 10", command = self.firstScan)
        scanButton.place(x = 50, y = 145)

        checkButton = Button(self.win, text = "무결성 검사", width = 10, height = 2, overrelief = "flat", font = "맑은고딕 10", command = self.integrityCheck)
        checkButton.place(x = 50, y = 215)

    def selectPath(self):
        selected_path = setFilePath()

        if selected_path:
            self.path.set(selected_path)
            self.output_filePath = os.path.join(self.path.get(), 'base_hash.txt')

            self.firstScan_result.set("") #새로운 경로가 선택되면 이전 값들을 초기화
            self.integrityCheck_result.set("")

    def firstScan(self):
        if not self.path.get():
            self.firstScan_result.set("스캔을 실패했습니다. 파일 경로를 먼저 선택해주세요.")
            return

        try:
            scan_results = scanDirectoryToTxt(self.path.get(), self.output_filePath)

            if scan_results:
                for item in scan_results:
                    if isinstance(item, tuple):
                        filePath, error = item

                        if error == "Permission Denied":
                            self.firstScan_result.set("스캔을 실패했습니다. 파일을 읽을 권한이 없습니다!")
                            return
                        elif error == "Error":
                            self.firstScan_result.set("스캔을 실패했습니다. 권한과 파일 경로 확인 후 다시 시도하세요!")
                            return
                    else:
                        continue
                
                self.firstScan_result.set("폴더 스캔을 완료했습니다.")
            else:
                self.firstScan_result.set("스캔을 실패했습니다. 권한과 파일 경로 확인 후 다시 시도하세요.")
        
        except FileNotFoundError:
            self.firstScan_result.set("스캔을 실패했습니다. 파일 경로를 재선택해주세요.")
        except PermissionError:
            self.firstScan_result.set("스캔을 실패했습니다. 파일을 읽을 권한이 없습니다!")
        except Exception as e:
            self.firstScan_result.set("스캔을 실패했습니다. 권한과 파일 경로 확인 후 다시 시도하세요!")

    def integrityCheck(self):
        if not self.path.get():
            self.integrityCheck_result.set("검사를 실패했습니다. 파일 경로를 먼저 선택해주세요.")
            return
        
        if not self.output_filePath or not os.path.exists(self.output_filePath):
            self.integrityCheck_result.set("검사를 실패했습니다. 최초 스캔을 먼저 해주세요.")
            return

        try: 
            current_hashes = scanDirectoryToDict(self.path.get()) #변경된 파일을 감지하기 위한 해시 값 불러오기

            check_results = Toplevel(self.win)
            check_results.title("무결성 검사 결과...")
            check_results.geometry("1000x500")

            scrollbar = Scrollbar(check_results) #검사 결과량을 고려한 스크롤바 생성
            scrollbar.pack(side = RIGHT, fill = Y)

            text = Text(check_results, yscrollcommand = scrollbar.set, wrap = "word", font = "맑은고딕 10") #새로운 창에 검사 결과 출력하기 위한 위젯 생성
            text.pack(side = LEFT, fill = BOTH, expand = True)

            text.tag_config("new", foreground = "green", font = "맑은고딕 10") #검사 결과 출력 색상 변경을 위한 태그 추가
            text.tag_config("change", foreground = "darkorange", font = "맑은고딕 10")
            text.tag_config("same", foreground = "blue", font = "맑은고딕 10")
            text.tag_config("delete", foreground = "red", font = "맑은고딕 10")
            text.tag_config("error", foreground = "orange", font = "맑은고딕 10")

            scrollbar.config(command = text.yview)

            check_results.transient(self.win) #검사 결과 창이 닫히기 전에 메인 프로그램 창을 제어할 수 없도록 설정
            check_results.grab_set()

            new, change, same, delete, error = compare_hashes(self.path.get(), self.output_filePath, current_hashes)

            for path in same:
                text.insert(END, "[동일한 파일] : " + path + "\n", "same")
                text.update_idletasks()
                text.see(END)
            for path in new:
                text.insert(END, "[생성된 파일] : " + path + "\n", "new")
                text.update_idletasks()
                text.see(END)
            for path in change:
                text.insert(END, "[변경된 파일] : " + path + "\n", "change")
                text.update_idletasks()
                text.see(END)
            for path in delete:
                text.insert(END, "[삭제된 파일] : " + path + "\n", "delete")
                text.update_idletasks()
                text.see(END)
            for path in error:
                text.insert(END, "[거부된 파일] : " + path + "\n", "error")
                text.update_idletasks()
                text.see(END)

            text.insert(END, f"\n\n동일한 파일 개수 : {len(same)}\n")
            text.insert(END, f"생성된 파일 개수 : {len(new)}\n")
            text.insert(END, f"변경된 파일 개수 : {len(change)}\n")
            text.insert(END, f"삭제된 파일 개수 : {len(delete)}\n")
            text.insert(END, f"거부된 파일 개수 : {len(error)}\n")

            text.see(END)
            text.config(state = DISABLED)

            self.integrityCheck_result.set("검사를 성공했습니다!")
        
        except FileNotFoundError:
            self.integrityCheck_result.set("검사를 실패했습니다. 최초 스캔을 먼저 해주세요.")
        except PermissionError:
            self.integrityCheck_result.set("검사를 실패했습니다. 파일을 읽을 권한이 없습니다!")
        except Exception as e:
            self.integrityCheck_result.set("검사를 실패했습니다. 권한과 파일 경로 확인 후 다시 시도하세요!")

    def run(self):
        self.win.mainloop()

if __name__ == "__main__": #gui_main.py가 직접 실행된 경우에만 실행
    app = GuiApp()
    app.run()