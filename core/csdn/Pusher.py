"""
自定义CSDN pusher
"""
import os
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.AbstractPusher import AbstractPusher


class Pusher(AbstractPusher):

    def getCookiePath(self, rootPath):
        return os.path.abspath(os.path.join(rootPath, 'csdn_cookie.json'))

    def write(self, driver, config, markdownProperties):
        try:
            # 输入标题
            title_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入文章标题（5~100个字）']"))
            )
            title_input.clear()
            title_input.send_keys(markdownProperties['title'])

            # 输入内容
            js = "document.querySelector('.editor__inner').textContent=`" + markdownProperties['content'] + "`"
            driver.execute_script(js)
            time.sleep(2)

            # 点击发布按钮
            publish_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn-publish"))
            )
            publish_button.click()

            # 延时等待填充下标签信息
            time.sleep(10)

        except TimeoutException:
            print('操作超时，请检查元素选择器是否正确')
