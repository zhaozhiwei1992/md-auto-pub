"""
约定优于配置

启动入口

python Main.py xxx.md platform
"""
from core.AbstractPusher import AbstractPusher
import sys

if __name__ == '__main__':
    # 获取命令行参数, 文件名
    if len(sys.argv) != 3:
        print('参数错误！')
        print('参数格式：python Main.py xx.md platform')
        print('例如: python Main.py xxx.md wechat')
        sys.exit()
    else:
        para_list = sys.argv
        print('Parameters is: ', para_list)
        if para_list[1].endswith('.md'):
            AbstractPusher().push(para_list[1], para_list[2])
