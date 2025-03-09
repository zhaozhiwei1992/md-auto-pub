"""
解析json配置信息, 转换为字典
"""
import json
import os


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
        try:
            with open(path, 'r', encoding='utf-8') as loadFile:
                jsonObj = json.load(loadFile)
                if jsonObj.get("ENABLE"):
                    return jsonObj
        except Exception as e:
            print(f"Error parsing file {path}: {e}")
        return {}

    def trans(self):
        allConfig = {}
        # 遍历目录, 返回所有有效配置
        # 获取项目根路径
        rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # 获取配置文件的路径
        confPath = os.path.abspath(os.path.join(rootPath, 'conf'))

        for filename in os.listdir(confPath):
            if filename.endswith(".json"):
                filePath = os.path.join(confPath, filename)
                obj = self.parse(filePath)
                if obj:
                    # 去掉文件名后缀.json
                    allConfig[filename[:-5]] = obj

        return allConfig
