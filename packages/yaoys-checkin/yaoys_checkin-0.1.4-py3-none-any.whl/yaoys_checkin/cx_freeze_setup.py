import sys
from cx_Freeze import setup, Executable

# 要打包的Python脚本路径
script = "AutoCheckIn.py"

# 创建可执行文件的配置
exe = Executable(
    script=script,
    base=None,
    targetName="AutoCheckIn"  # 生成的可执行文件名称
)

# 打包的参数配置
options = {
    "build_exe": {
        "packages": ['apscheduler'],
        "excludes": [],
        'include_files': ['D:\\Anaconda3\\envs\\autocheckin\\Lib\\site-packages\\sklearn\\.libs\\vcomp140.dll',
                          'D:\\Anaconda3\\envs\\autocheckin\\Lib\\site-packages\\pyzmq.libs\\msvcp140.dll']
    }
}

setup(
    name="AutoCheckIn",
    version="0.1.3",
    description="AutoCheckIn",
    options=options,
    executables=[exe]
)
