from core_scan.scan import scanDirectoryToTxt, scanDirectoryToDict
from load_hashes.compare_hashes import compare_hashes
import sys, os

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
END = '\033[0m'

class TerminalApp:
    def __init__(self, argv):
        self.action = sys.argv[1]
        self.filePath = sys.argv[2]
        self.output_filePath = os.path.join(self.filePath, 'base_hash.txt')
    
    def firstScan(self):
        try:
            print(f"\n\n[{self.filePath}] 폴더를 스캔합니다...\n")
            scan_results = scanDirectoryToTxt(self.filePath, self.output_filePath)

            if scan_results:
                for item in scan_results:
                    if isinstance(item, tuple):
                        filePath, error = item

                        if error == "Permission Denied":
                            print(f"{RED}[실패] 파일을 읽을 권한이 없습니다! : {filePath}{END}")
                        elif error == "Error":
                            print(f"{RED}[실패] 알 수 없는 오류가 발생했습니다! : {filePath}{END}")
                    
                    else:
                        print(f"{GREEN}[성공] 해시 값 계산 완료 : {item}{END}")
                
                print(f"\n[{self.filePath}] 폴더 스캔을 완료했습니다. 결과가 '{self.output_filePath}' 에 저장되었습니다.\n")
            else:
                print(f"{RED}[오류] {self.filePath} : 알 수 없는 오류가 발생했습니다.{END}\n")

        except FileNotFoundError:
            print(f"{RED}[오류] {self.filePath} 파일을 찾을 수 없습니다.{END}\n")
        except PermissionError:
            print(f"{RED}[오류] {self.filePath} 파일을 읽을 권한이 없습니다.{END}\n")
        except Exception as e:
            print(f"{RED}[오류] {self.filePath} : 알 수 없는 오류가 발생했습니다.{END}\n")
    
    def integrityCheck(self):
        try:
            current_hashes = scanDirectoryToDict(self.filePath) #변경된 파일을 감지하기 위한 해시 값 불러오기

            print(f"\n\n===== [{self.filePath}] 폴더 무결성 검사 결과 =====\n")
            new, change, same, delete, error = compare_hashes(self.filePath, self.output_filePath, current_hashes)

            for path in same:
                print(f'{BLUE}[동일한 파일] : {path}{END}')
            for path in new:
                print(f'{GREEN}[생성된 파일] : {path}{END}')
            for path in change:
                print(f'{YELLOW}[변경된 파일] : {path}{END}')
            for path in delete:
                print(f'{RED}[삭제된 파일] : {path}{END}')
            for path in error:
                print(f'{MAGENTA}[거부된 파일] : {path}{END}')
            print()
            
        except FileNotFoundError:
            print(f"{RED}[오류] '{self.filePath}'의 최초 스캔을 먼저 해주세요.{END}\n")
        except PermissionError:
            print(f"{RED}[오류] {self.filePath} 파일을 읽을 권한이 없습니다.{END}\n")
        except Exception as e:
            print(f"{RED}[오류] {self.filePath} : 알 수 없는 오류가 발생했습니다.{END}\n")
            
    def run(self):     
        if self.action == 'scan':
            self.firstScan()
        elif self.action == 'check':
            self.integrityCheck()
        else:
            print(f"{RED}[오류] scan/check 키워드를 정확히 입력하세요!\n{END}")


if __name__ == "__main__": #main.py가 직접 실행된 경우에만 실행
    if len(sys.argv) != 3:
            print(f"{RED}[오류] scan/check와 파일 경로를 하나씩 입력하세요!\n{END}")
            sys.exit()

    app = TerminalApp(sys.argv)

    app.run()