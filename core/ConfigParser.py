"""
解析json配置信息, 转换为字典
"""
import json

class ConfigParser:

    # 解析json转换为dict
    def parse(self, path):
        # json.JSONDecoder()
        pass

    def trans(self):
        allConfig = {}
        # 遍历目录, 返回所有有效配置
        self.parse("zhihu.json")
        return allConfig
