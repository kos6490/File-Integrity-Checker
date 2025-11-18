import hashlib
import os


def scanDirectoryToTxt(
    scan_dir, output_filePath
):  # 최초 스캔, 결과를 .base_hash에 저장
    success_filePath = list()
    try:
        with open(output_filePath, "w", encoding="utf-8") as f_out:
            for path, dir, files in os.walk(scan_dir):
                for file in files:
                    if file == ".base_hash":
                        continue

                    filePath = os.path.join(path, file)

                    try:
                        hash_object = hashlib.sha256()

                        with open(filePath, "rb") as f_in:
                            while chunk := f_in.read(4096):
                                hash_object.update(chunk)

                        hash_result = hash_object.hexdigest()

                        f_out.write(f"{filePath} : {hash_result}\n")
                        success_filePath.append(filePath)

                    except PermissionError:
                        f_out.write(f"{filePath} : Permission Denied\n")
                        success_filePath.append((filePath, "Permission Denied"))
                    except Exception as e:
                        f_out.write(f"{filePath} : Error ({e})\n")
                        success_filePath.append((filePath, "Error"))

        return success_filePath

    except FileNotFoundError:
        raise FileNotFoundError
    except Exception as e:
        raise Exception(e)


def scanDirectoryToDict(
    scan_dir,
):  # 변경된 파일을 감지하기 위한 스캔, 결과를 딕셔너리로 반환
    try:
        hash_dict = {}

        for path, dir, files in os.walk(scan_dir):
            for file in files:
                if file == ".base_hash":
                    continue

                filePath = os.path.join(path, file)

                try:
                    hash_object = hashlib.sha256()

                    with open(filePath, "rb") as f:
                        while chunk := f.read(4096):
                            hash_object.update(chunk)

                    hash_result = hash_object.hexdigest()

                    filePath = os.path.normpath(filePath)

                    hash_dict[filePath] = hash_result

                except PermissionError:
                    hash_dict[filePath] = "Permission Denied"
                except Exception as e:
                    hash_dict[filePath] = "Error"

        return hash_dict

    except FileNotFoundError:
        raise FileNotFoundError
    except Exception as e:
        raise Exception(e)
