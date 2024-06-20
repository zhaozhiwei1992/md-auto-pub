"""
自定义知乎, Pusher
"""
import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Pusher:

    def getCookiePath(self, rootPath):
        return os.path.abspath(rootPath + 'cookie/zhihu_cookie.json')

    def write(self, driver, config, markdownProperties):
        try:
            # 输入标题
            title_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "title"))
            )
            title_input.clear()
            title_input.send_keys(markdownProperties['title'])

            # 输入内容
            content_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*/textarea'))
            )
            content_input.clear()
            content_input.send_keys(markdownProperties['content'])


            # 点击发布按钮`
            publish_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@class='xitu-btn']"))
            )
            publish_button.click()

        except TimeoutException:
            print('操作超时，请检查元素选择器是否正确')
