import hashlib
import os
import zipfile


def CalFileMD5(path):
    size = os.path.getsize(path)  # 获取文件大小，单位是字节（byte）
    algorithm = hashlib.md5()
    with open(path, 'rb') as f:  # 以二进制模式读取文件
        while size >= 1024 * 1024:  # 当文件大于1MB时将文件分块读取
            algorithm.update(f.read(1024 * 1024))
            size -= 1024 * 1024
        algorithm.update(f.read())

    return algorithm.hexdigest()  

def MakePath(targetPath):
    targetCheckPath:str = targetPath.replace('\\', '/')
    dotPos = targetCheckPath.rfind('.')
    lastPathPos = targetCheckPath.rfind('/')

    if dotPos > 0 and lastPathPos < dotPos:
        targetCheckPath = targetCheckPath[0: lastPathPos]
    
    if os.path.exists(targetCheckPath):
        return
        
    subPaths = targetCheckPath.split('/')
    curCheckPath = ""
    subPathCount = len(subPaths)

    for i in range(0, subPathCount):
        curCheckPath += subPaths[i] + "/"
        if not os.path.exists(curCheckPath):
            os.makedirs(curCheckPath)

# 删除整个文件夹
def DeleteFolder(path):
    if not os.path.exists(path):
        return

    for root, dirs, files in os.walk(path, topdown=False):
        for f in files:
            os.remove(os.path.join(root, f))
        for folder in dirs:
            os.rmdir(os.path.join(root, folder))

    os.rmdir(path)
    return


def DeleteFile(filePath):
    if os.path.isfile(filePath):
        os.remove(filePath)
    return


# 删除文件夹里的所有文件
def CleanFolder(path):
    if not os.path.exists(path):
        return

    for root, dirs, files in os.walk(path, topdown=False):
        for f in files:
            os.remove(os.path.join(root, f))
        for folder in dirs:
            os.rmdir(os.path.join(root, folder))
    return


# 压缩文件夹
def Zip(folderPath, zipFilePath):

    filelist = []

    if os.path.isfile(folderPath):
        filelist.append(folderPath)
    else:
        for root, dirs, files in os.walk(folderPath):
            for name in files:
                filelist.append(os.path.join(root, name))

    MakePath(zipFilePath)
    zf = zipfile.ZipFile(zipFilePath, "w", zipfile.zlib.DEFLATED)

    for tar in filelist:
        arcname = tar[len(folderPath):]
        # print arcname
        zf.write(tar, arcname)

    zf.close()

# 解压文件夹
def Unzip(zipFilePath, exportPath):

    unziptodir = exportPath.replace('\\', '/')

    zfobjs = zipfile.ZipFile(zipFilePath)

    for curFilePath in zfobjs.namelist():
        curFilePath = curFilePath.replace('\\', '/')
        targetFilePath = unziptodir + '/' + curFilePath
        MakePath(targetFilePath)
        open(unziptodir + '/' + curFilePath,
             "wb").write(zfobjs.read(curFilePath))

def Join(path, *paths):
    return os.path.join(path, *paths).replace("\\", "/")