import os

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
END = '\033[0m'

def readBaseHash(base_hash_filePath):
    try:
        hash_dict = {}

        with open(base_hash_filePath, 'r', encoding = 'utf-8') as f:
            for line in f:
                if ' : ' in line:
                    key, value = line.split(' : ', 1)
                    key = key.strip()
                    value = value.strip()
                    key = os.path.normpath(key)

                    hash_dict[key] = value

        return hash_dict
    
    except FileNotFoundError:
        print(f"{RED}[오류] {base_hash_filePath} 파일을 찾을 수 없습니다.{END}\n")
    except Exception as e:
        print(f"{RED}[오류] {base_hash_filePath} : 알 수 없는 오류가 발생했습니다.{END}\n")