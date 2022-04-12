"""
登录后存储cookie信息, 后续处理最好也都依赖cookie保持统一
"""

import webbrowser
import json


class Login:

    # 登录
    # 通过cookie信息, 传入到selenium中
    def login(self, config):
        # 判断如果不存在cookie则去登录
        if (not self.isCookieExists(config)):
            # 登录成功后写入cookie, 刷新本地配置
            pass

        self.getCookie()

    def isCookieExists(self, url):
        with open('cookie/cookie.txt', 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())
        print('%%%%%%%%%%%%%%%%%', listCookies)
        for cookie in listCookies:
            webbrowser.add_cookie(cookie)
        #     判断是否存在
        webbrowser.get(url)

    # 获取浏览器cookie信息，并保存到指定目录
    def getCookie(self):
        dictCookies = webbrowser.get_cookies()
        jsonCookies = json.dumps(dictCookies)
        # print(jsonCookies)
        with open('cookie/cookie.txt', 'w') as f:
            f.write(jsonCookies)
        pass
