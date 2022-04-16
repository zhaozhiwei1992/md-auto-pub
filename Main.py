"""
约定优于配置

启动入口

python Main.py xxx.md
"""
from core.AbstractPusher import AbstractPusher
import sys

if __name__ == '__main__':
    # 获取命令行参数, 文件名
    if len(sys.argv) == 1:
        print('请指定markdown文件!')
        sys.exit()
    else:
        para_list = sys.argv
        print('Parameters is: ', para_list)
        if para_list[1].endswith('.md'):
            AbstractPusher().push(para_list[1])
