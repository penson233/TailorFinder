#读取文件
def readdomain(filepath):
    with open(filepath,'r') as f:
        read = f.readlines()
    return read