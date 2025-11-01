import os

filePath = '../temp'

for (path, dir, file) in os.walk(filePath):
    print("PATH : ", path)
    print("DIR : ", dir)
    print("FILE : ", file)
    print('----------------------------------------------------------')