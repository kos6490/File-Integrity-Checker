#sha256 + os_walk logic

import hashlib
import os

scan_dir = '../temp'
output_filePath = '../temp/base_hash.txt'

try:
    with open(output_filePath, 'w', encoding = 'utf-8') as f_out:
        print(f"[{scan_dir}] 폴더를 스캔합니다...")

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
                    print(f"[성공] 해시 값 계산 완료 : {filePath}")

                except PermissionError:
                    print(f"[오류] {filePath} 파일을 읽을 권한이 없습니다.")
                    f_out.write(f"{filePath} : Permission Denied\n")
                except Exception as e:
                    print(f"[오류] {filePath} 알 수 없는 오류가 발생했습니다.")
                    f_out.write(f"{filePath} : Error ({e})\n")

    print(f"[{scan_dir}] 폴더 스캔을 완료했습니다. 결과가 '{output_filePath}' 에 저장되었습니다.")

except FileNotFoundError:
    print(f"[오류] {filePath} 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"[오류] {filePath} 알 수 없는 오류가 발생했습니다.")