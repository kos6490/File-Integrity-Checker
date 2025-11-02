#sha256 + os_walk logic

import hashlib
import os

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
END = '\033[0m'

def scanDirectoryToTxt(scan_dir, output_filePath): #최초 스캔, 결과를 base_hash.txt에 저장
    try:
        with open(output_filePath, 'w', encoding = 'utf-8') as f_out:
            print(f"[{scan_dir}] 폴더를 스캔합니다...\n")

            for path, dir, files in os.walk(scan_dir):
                for file in files:
                    if file == 'base_hash.txt':
                        continue

                    filePath = os.path.join(path, file)

                    try:
                        hash_object = hashlib.sha256()

                        with open(filePath, 'rb') as f_in:
                            while chunk := f_in.read(4096):
                                hash_object.update(chunk)

                        hash_result = hash_object.hexdigest()

                        f_out.write(f"{filePath} : {hash_result}\n")
                        print(f"{GREEN}[성공] 해시 값 계산 완료 : {filePath}{END}")

                    except PermissionError:
                        print(f"{RED}[오류] {filePath} 파일을 읽을 권한이 없습니다.{END}\n")
                        f_out.write(f"{filePath} : Permission Denied\n")
                    except Exception as e:
                        print(f"{RED}[오류] {filePath} : 알 수 없는 오류가 발생했습니다.{END}\n")
                        f_out.write(f"{filePath} : Error ({e})\n")

        print(f"\n[{scan_dir}] 폴더 스캔을 완료했습니다. 결과가 '{output_filePath}' 에 저장되었습니다.\n")

    except FileNotFoundError:
        print(f"{RED}[오류] {filePath} 파일을 찾을 수 없습니다.{END}\n")
    except Exception as e:
        print(f"{RED}[오류] {filePath} : 알 수 없는 오류가 발생했습니다.{END}\n")

def scanDirectoryToDict(scan_dir): #변경된 파일을 감지하기 위한 스캔, 결과를 딕셔너리로 반환
    try:
        hash_dict = {}

        for path, dir, files in os.walk(scan_dir):
            for file in files:
                if file == 'base_hash.txt':
                    continue

                filePath = os.path.join(path, file)

                try:
                    hash_object = hashlib.sha256()

                    with open(filePath, 'rb') as f:
                        while chunk := f.read(4096):
                            hash_object.update(chunk)

                    hash_result = hash_object.hexdigest()

                    filePath = os.path.normpath(filePath)

                    hash_dict[filePath]=hash_result

                except PermissionError:
                    print(f"{RED}[오류] {filePath} 파일을 읽을 권한이 없습니다.{END}\n")
                except Exception as e:
                    print(f"{RED}[오류] {filePath} : 알 수 없는 오류가 발생했습니다.{END}\n")

        return hash_dict

    except FileNotFoundError:
        print(f"{RED}[오류] {filePath} 파일을 찾을 수 없습니다.{END}\n")
    except Exception as e:
        print(f"{RED}[오류] {filePath} : 알 수 없는 오류가 발생했습니다.{END}\n")
