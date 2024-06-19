"""
自定义知乎, Pusher
"""
import os
import time

import pyautogui
import pyperclip
from selenium.common.exceptions import TimeoutException


class Pusher:

    def getCookiePath(self, rootPath):
        return os.path.abspath(rootPath + 'cookie/zhihu_cookie.json')

    # 录入内容,
    def write(self, driver, config, markdownProperties):
        # 写文章界面
        # 标题 x=505, y=294
        time.sleep(3)
        pyautogui.click(x=505, y=294, button='left')
        time.sleep(2)
        pyperclip.copy(markdownProperties['title'])
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')

        # 正文
        # 知乎目前不支持直接输入markdown, 所以转换后给它塞进去, 懒得整它的导入了
        # 跳转到转换页面，把markdown进行格式转换
        transMdUrl = config.get("TRANS_MD")
        pyperclip.copy(markdownProperties['content'])
        # 打开转换页面 https://md.phodal.com/
        js = "window.open('{}','_blank');"
        time.sleep(2)
        try:
            driver.execute_script(js.format(transMdUrl))
        except TimeoutException:
            print('timeout')
        # 写入左侧页面 x=182, y=263
        time.sleep(2)
        pyautogui.click(x=182, y=263, button='left')
        time.sleep(2)
        # 全选 /删除
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(2)
        pyautogui.hotkey('backspace')
        # 将markdown内容写入到左侧
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')

        # 点击复制 并复制到剪贴板 x=857, y=170
        time.sleep(1)
        pyautogui.click(x=857, y=170, button='left')
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'c')

        # 回到主页签, 第一个
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])

        # 定位到内容区, 写入转换内容 x=516, y=409
        time.sleep(2)
        pyautogui.click(x=516, y=409, button='left')
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')

        # 发布设置 x=429, y=860
        time.sleep(1)
        pyautogui.click(x=429, y=860, button='left')
        # 文章话题/添加话题x=581, y=782
        time.sleep(1)
        pyautogui.click(x=581, y=782, button='left')
        # 光标定位录入框
        time.sleep(1)
        pyautogui.click(x=581, y=782, button='left')
        # 录入一个后选择搜索内容
        tags = str(markdownProperties['tag'])
        tagList = tags.split(",")
        pyperclip.copy(tagList[0])
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        # 选择搜索结果最上边的 x=554, y=613
        pyautogui.click(x=554, y=613, button='left')

        # 发布 x=1170, y=862
        time.sleep(2)
        # pyautogui.click(x=1170, y=862, button='left')