import hashlib

filePath = '../temp/temp.txt'
hash_object = hashlib.sha256()

try:
    with open(filePath, 'rb') as f:
        while chunk := f.read(4096): #파일을 4096바이트씩 chunk로 가져옴, 대용량 파일 고려
            hash_object.update(chunk)

    hash_result = hash_object.hexdigest()

    with open('../temp/hash.txt', 'a', encoding = 'utf-8') as f:
        f.write(f"{filePath} : {hash_result}\n")

    print(f"해시 값 계산 완료 : {filePath} : {hash_result}")

except FileNotFoundError:
    print(f"오류 : {filePath} 파일을 찾을 수 없습니다.")