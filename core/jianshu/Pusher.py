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


class Pusher(AbstractPusher):

    def getCookiePath(self, rootPath):
        return os.path.abspath(os.path.join(rootPath, 'jianshu_cookie.json'))

    def write(self, driver, config, markdownProperties):
        try:
            # 等待页面加载并找到写文章按钮
            write_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'write-btn'))
            )
            write_button.click()

            # 点击写文章后会跳转新页签，切换到新页签
            WebDriverWait(driver, 10).until(EC.new_window_is_opened(driver.window_handles))
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(10)

            # 等待并点击新建文章按钮
            new_article_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'fa-plus-circle'))
            )
            new_article_button.click()
            time.sleep(10)

            # 输入标题
            title_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ul[@class='clearfix']/preceding-sibling::div[1]"))
            )
            title_input.clear()
            title_input.send_keys(markdownProperties['title'])

            # 输入内容
            content_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'arthur-editor'))
            )
            content_input.clear()
            content_input.send_keys(markdownProperties['content'])

            # 点击发布按钮
            publish_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'fa fa-mail-forward'))
            )
            publish_button.click()

        except TimeoutException:
            print('操作超时，请检查元素选择器是否正确')
