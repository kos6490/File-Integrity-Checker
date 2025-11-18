from load_hashes.read_hashes import readBaseHash
import sys, os


def compare_hashes(scan_dir, output_filePath, current_hashes):
    try:
        past_hashes = readBaseHash(output_filePath)  # base_hash.txt 해시 값 불러오기

        potential_new = {}
        potential_delete = {}
        new = list()
        change = list()
        same = list()
        delete = list()
        rename = list()
        error = list()

        for path, hash in current_hashes.items():
            if hash == "Permission Denied" or hash == "Error":
                error.append(path)
                continue

            if path not in past_hashes:
                potential_new[path] = hash
            elif past_hashes[path] != hash:
                change.append(path)
            else:
                same.append(path)

        for path, hash in past_hashes.items():
            if path not in current_hashes:
                potential_delete[path] = hash

        deleted_hashes = {hash: path for path, hash in potential_delete.items()}

        for path, hash in potential_new.items():
            if hash in deleted_hashes:
                old_path = deleted_hashes[hash]
                rename.append(f"{old_path} -> {path}")
                del potential_delete[old_path]
                del deleted_hashes[hash]
            else:
                new.append(path)

        delete = list(potential_delete.keys())

        return new, change, same, delete, rename, error

    except FileNotFoundError:
        raise FileNotFoundError
    except Exception as e:
        raise Exception(e)
