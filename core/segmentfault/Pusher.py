"""
思否自动提交实现
"""
from selenium import webdriver
import json
import os
import time
import pyautogui
import pyperclip


class Pusher:

    def getCookiePath(self, rootPath):
        return os.path.abspath(rootPath + 'cookie/segmentfault_cookie.json')

    # 录入内容,
    # 这部分根据实际情况调整坐标
    def write(self, config, markdownProperties):

        # 撰写 x=1171, y=155
        time.sleep(3)
        pyautogui.click(x=1171, y=155, button='left')

        # 写文章 x=1178, y=230
        time.sleep(3)
        pyautogui.click(x=1178, y=230, button='left')

        # 可能有弹框提示 x掉 x=1021, y=186
        time.sleep(3)
        pyautogui.click(x=1021, y=186, button='left')

        # 标题 x=210, y=233
        time.sleep(3)
        pyautogui.click(x=210, y=233, button='left')
        time.sleep(2)
        pyperclip.copy(markdownProperties['title'])

        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')

        # 添加标签 x=77, y=288
        time.sleep(2)
        pyautogui.click(x=77, y=288, button='left')
        # 搜索标签 x=144, y=367
        time.sleep(2)
        pyautogui.click(x=144, y=367, button='left')
        # 输入标签 回车, 每次只能录入一个
        time.sleep(1)
        # tags = str(markdownProperties['tag'])
        # tagList = tags.split(",")
        # for tag in tagList:
        #     pyperclip.copy(tag)
        #     time.sleep(2)
        #     pyautogui.hotkey('ctrl', 'v')
        # 标签不存在无法添加,随意指定其他
        pyperclip.copy("其他")
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.hotkey('enter')
        # 这里留点时间30s, 可以加其它标签
        # time.sleep(30)

        # 内容区 x=339, y=689
        time.sleep(3)
        pyautogui.click(x=339, y=689, button='left')

        time.sleep(1)
        pyperclip.copy(markdownProperties['content'])
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'v')

        # 发布文章 x=1501, y=153
        time.sleep(2)
        pyautogui.click(x=1501, y=153, button='left')

        # 确认发布 x=1384, y=624
        time.sleep(2)
        pyautogui.click(x=1384, y=624, button='left')
