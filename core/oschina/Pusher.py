"""
自定义博客园 pusher, 继承core.AbstractPusher
"""
import os
import time

import pyautogui
import pyperclip


class Pusher:

    def getCookiePath(self, rootPath):
        return os.path.abspath(os.path.join(rootPath, 'oschina_cookie.json'))

    # 录入内容,
    # 这部分根据实际情况调整坐标
    def write(self, config, markdownProperties):
        time.sleep(3)
        # 写博客 1027, 211
        pyautogui.click(x=1027, y=211, button='left')

        # 通过pyautogui 定位到标题, 写入内容
        time.sleep(3)
        pyperclip.copy(markdownProperties['title'])

        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')

        # 切换为markdown模式 373, 334
        time.sleep(2)
        pyautogui.click(x=373, y=334, button='left')

        # 通过pyautogui 定位到内容区, 写入内容
        time.sleep(2)
        pyperclip.copy(markdownProperties['content'])
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'v')

        # 通过pyautogui获取到提交按钮, 点击发布
        time.sleep(3)
        # 发布文章 x=1328, y=276
        pyautogui.click(x=1328, y=276, button='left')
        # 确认发布 x=1288, y=505
        time.sleep(3)
        pyautogui.click(x=1288, y=505, button='left')
