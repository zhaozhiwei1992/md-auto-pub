"""
自定义博客园 pusher, 继承core.AbstractPusher
"""
import os
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.AbstractPusher import AbstractPusher

import pyautogui
import pyperclip


class Pusher(AbstractPusher):

    def getCookiePath(self, rootPath):
        return os.path.abspath(os.path.join(rootPath, 'juejin_cookie.json'))

    def write(self, driver, config, markdownProperties):
        # tab键到内容
        # 发布按钮 1414, 162
        # 分类 1081, 296
        # 添加标签 1103, 411
        # 选择标签 1052, 525
        # 摘要 1115, 734
        # 默认会根据文章自动写入, 30秒内自己调整
        # 确认发布 1411, 867
        try:

            # 输入内容
            # content_input = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.TAG_NAME, "textarea"))
            # )
            # content_input.clear()
            # content_input.send_keys(markdownProperties['content'])
            time.sleep(2)
            pyperclip.copy(markdownProperties['content'])
            time.sleep(3)
            pyautogui.hotkey('ctrl', 'v')

            # 输入标题
            title_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "title-input"))
            )
            title_input.clear()
            title_input.send_keys(markdownProperties['title'])

            # 点击发布按钮
            publish_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@class='xitu-btn']"))
            )
            publish_button.click()

            # 等待输入标签
            time.sleep(20)

        except TimeoutException:
            print('操作超时，请检查元素选择器是否正确')
