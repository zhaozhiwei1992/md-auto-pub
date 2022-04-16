"""
解析json配置信息, 转换为字典
"""
import os
import json


class ConfigParser:

    # 解析json转换为dict
    # {
    #     "ENABLE": true,
    #     "USERNAME": "你的账号",
    #     "PASSWORD": "你的密码",
    #     "LOGIN_URL": "https://www.zhihu.com/signin?next=%2F",
    #     "WRITE_URL": "https://zhuanlan.zhihu.com/write"
    # }
    def parse(self, path):
        with open(path, 'r') as loadFile:
            jsonObj = json.load(loadFile)
            if jsonObj.get("ENABLE"):
                return jsonObj
            else:
                return {}

    def trans(self):
        allConfig = {}
        # 遍历目录, 返回所有有效配置

        curPath = os.path.abspath(os.path.dirname(__file__))
        # MdAutoPub，也就是项目的根路径
        rootPath = curPath[:curPath.find("MdAutoPub/") + len("MdAutoPub/")]
        # 获取xx.md文件的路径
        confPath = os.path.abspath(rootPath + 'conf/')
        for filename in os.listdir(confPath):
            obj = self.parse(confPath + "/" + filename)
            if len(obj.keys()) > 0:
                # 去掉文件名后缀.json
                allConfig[filename[:-5]] = obj
        return allConfig
