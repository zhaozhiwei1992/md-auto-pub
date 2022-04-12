"""
自定义博客园 pusher, 继承core.AbstractPusher
"""
from core.AbstractPusher import AbstractPusher
import webbrowser
import json


class Pusher(AbstractPusher):

    # 扩展实现入口
    def pushExt(self, config, markdownProperties):
        self.login()
        self.forward(markdownProperties.get("WRITE_URL"))
        self.write(markdownProperties)
        self.submit()
        pass

    def login(self):
        with open('cookie/cookie.txt', 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())
        print('%%%%%%%%%%%%%%%%%', listCookies)
        for cookie in listCookies:
            webbrowser.add_cookie(cookie)

    def forward(self, url):
        # 获取cookie
        webbrowser.get(url)
        # 跳转到指定页面
        webbrowser.open(url)
        # 读取完cookie刷新页面
        # webbrowser.refresh()

    def write(self):
        # 录入内容
        # 可能涉及一些特殊内容解析
        pass

    def submit(self):
        # 获取到提交按钮, 点击发布
        pass
