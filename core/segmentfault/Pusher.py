"""
思否自动提交实现
"""
import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.AbstractPusher import AbstractPusher


class Pusher(AbstractPusher):

    def getCookiePath(self, rootPath):
        return os.path.abspath(os.path.join(rootPath, 'segmentfault_cookie.json'))

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
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/div[2]/div/div/div/div[1]/div[2]/div[1]/div[3]/div/div/div[1]/textarea'))
            )
            content_input.clear()
            content_input.send_keys(markdownProperties['content'])

            # 添加标签
            # tag_input = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, "//input[@class='publishBtn']"))
            # )

            # 点击发布按钮`
            publish_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@class='xitu-btn']"))
            )
            publish_button.click()

        except TimeoutException:
            print('操作超时，请检查元素选择器是否正确')
