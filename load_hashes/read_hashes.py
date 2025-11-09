import os

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
        raise FileNotFoundError
    except Exception as e:
        raise Exception(e)