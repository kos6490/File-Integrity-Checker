from load_hashes.read_hashes import readBaseHash
import sys, os

def compare_hashes(scan_dir, output_filePath, current_hashes):
    try:
        past_hashes = readBaseHash(output_filePath) #base_hash.txt 해시 값 불러오기

        new = list()
        change = list()
        same = list()
        delete = list()
        error = list()

        for path, hash in current_hashes.items():
            if hash == "Permission Denied" or hash == "Error":
                error.append(path)
                continue
            
            if path not in past_hashes:
                new.append(path)
            elif past_hashes[path] != hash:
                change.append(path)
            else :
                same.append(path)
        
        for path, hash in past_hashes.items():
            if path not in current_hashes:
                delete.append(path)
    
        return new, change, same, delete, error

    except FileNotFoundError:
        raise FileNotFoundError
    except Exception as e:
        raise Exception(e)
