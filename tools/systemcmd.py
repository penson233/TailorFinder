import os
import subprocess
def runshell(cmd,name):
    print(cmd,name)
    os.system(cmd)


def subpross(cmd):

    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 检查命令是否成功执行
    if result.returncode == 0:

        # 输出命令的标准输出
        return result.stdout
    else:
        print("命令执行失败")
        # 输出命令的标准错误
        print("错误:\n", result.stderr)
        return None