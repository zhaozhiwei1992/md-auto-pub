"""
自定义CSDN pusher
"""
import os
import time

import pyautogui
import pyperclip


class Pusher:

    def getCookiePath(self, rootPath):
        return os.path.abspath(rootPath + 'cookie/csdn_cookie.json')

    # 录入内容,
    # 这部分根据实际情况调整坐标
    def write(self, config, markdownProperties):

        # x掉模板库弹框 x=1139, y=266
        time.sleep(3)
        pyautogui.click(x=1139, y=266, button='left')

        # 标题 x=317, y=156
        time.sleep(3)
        pyautogui.click(x=317, y=156, button='left')
        time.sleep(1)
        pyperclip.copy(markdownProperties['title'])
        # 覆盖原标题
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')

        # 内容区x=186, y=366
        time.sleep(3)
        pyautogui.click(x=186, y=366, button='left')
        time.sleep(1)
        pyperclip.copy(markdownProperties['content'])
        # 覆盖原标题
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')

        # 发布文章 x=1442, y=150
        time.sleep(2)
        pyautogui.click(x=1442, y=150, button='left')

        # 文章标签 x=578, y=527
        # 标签无法自定义的话时间拉长，手选了只能
        time.sleep(2)
        pyautogui.click(x=578, y=527, button='left')
        time.sleep(2)
        pyautogui.click(x=604, y=609, button='left')
        time.sleep(2)
        pyperclip.copy("其他")
        time.sleep(2)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(5)
        pyautogui.click(x=594, y=664, button='left')
        # 移除弹框
        time.sleep(3)
        pyautogui.click(x=486, y=623, button='left')

        # 文章类型x=551, y=626
        time.sleep(3)
        pyautogui.click(x=551, y=626, button='left')

        # 发布形式 x=551, y=727
        time.sleep(3)
        pyautogui.click(x=551, y=727, button='left')

        # 内容等级 x=648, y=776
        time.sleep(3)
        pyautogui.click(x=648, y=776, button='left')

        # 确认发布 x=1084, y=833
        time.sleep(3)
        pyautogui.click(x=1084, y=833, button='left')
