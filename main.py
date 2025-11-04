from core_scan.scan import scanDirectoryToTxt
from load_hashes.compare_hashes import compare_hashes
import sys, os

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
END = '\033[0m'

if len(sys.argv) > 3:
    print(f"{RED}[오류] scan/check와 파일 경로를 하나씩 입력하세요!\n{END}")
    sys.exit()
elif 0 <= len(sys.argv) <= 2:
    print(f"{RED}[오류] scan/check와 파일 경로를 하나씩 입력하세요!\n{END}")
    sys.exit()

filePath = sys.argv[2]
output_filePath = os.path.join(filePath, 'base_hash.txt')

if sys.argv[1] == 'scan':
    scanDirectoryToTxt(filePath, output_filePath)
elif sys.argv[1] == 'check':
    compare_hashes(filePath, output_filePath)
else:
    print(f"{RED}[오류] scan/check 키워드를 정확히 입력하세요!\n{END}")