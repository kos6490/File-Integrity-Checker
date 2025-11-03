import sys, os

#scan.py 파일의 scanDirectoryToDict 함수 사용을 위한 폴더 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from load_hashes.read_hashes import readBaseHash
from core_scan.scan import scanDirectoryToDict

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
END = '\033[0m'

def compare_hashes(scan_dir, output_filePath):
    past_hashes = readBaseHash(output_filePath) #base_hash.txt 해시 값 불러오기
    current_hashes = scanDirectoryToDict(scan_dir) #변경된 파일을 감지하기 위한 해시 값 불러오기

    print(f"\n===== [{scan_dir}] 폴더 무결성 검사 결과 =====\n")

    for path, hash in current_hashes.items():
        if path not in past_hashes:
            print(f'{GREEN}[생성된 파일] : {path}{END}')
        elif past_hashes[path] != hash:
            print(f'{YELLOW}[변경된 파일] : {path}{END}')
        else :
            print(f'{BLUE}[동일한 파일] : {path}{END}')
        
    for path, hash in past_hashes.items():
        if path not in current_hashes:
            print(f'{RED}[삭제된 파일] : {path}{END}')
    
    print()