"""
自定义博客园 pusher, 继承core.AbstractPusher
"""
import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.AbstractPusher import AbstractPusher

import time

import pyautogui
import pyperclip


class Pusher(AbstractPusher):

    def getCookiePath(self, rootPath):
        return os.path.abspath(os.path.join(rootPath, 'wechat_cookie.json'))

    def write(self, driver, config, markdownProperties):
        try:
            # 打开新页签， 通过https://md.phodal.com/转换markdown然后获取内容
            main_window = driver.current_window_handle
            driver.execute_script("window.open('');")
            # 切换到新标签页
            new_window = [window for window in driver.window_handles if window != main_window][0]
            driver.switch_to.window(new_window)
            # 在新标签页中加载指定 URL
            driver.set_page_load_timeout(2)  # 增加页面加载超时时间为10秒
            try:
                driver.get(config["TRANS_MD"])
            except TimeoutException:
                print('timeout')

            # 获取界面一些操作
            content_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="input"]'))
            )
            content_input.clear()
            # 打开上述网站将markdown内容贴入
            markdownContent = markdownProperties['content']
            content_input.send_keys(markdownContent)
            # 点击复制按钮
            copy_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@data-clipboard-action='cut']"))
            )
            copy_button.click()
            # 复制转换后的内容
            time.sleep(2)
            pyautogui.hotkey('ctrl', 'c')

            # content = ""
            # 回到之前页面
            driver.switch_to.window(main_window)
            # 输入内容,光标此时就在文本框，粘贴即可

            # 公众号那个session没啥用，还是得登录一次
            time.sleep(30)

            # 跳转新建文章
            # 点击复制按钮
            new_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[3]/div[2]/div/div[2]/div'))
            )
            new_button.click()

            time.sleep(5)
            pyautogui.hotkey('ctrl', 'v')

            # 输入标题
            title_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="title"]'))
            )
            title_input.clear()
            title_input.send_keys(markdownProperties['title'])

            # 输入作者
            title_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="author"]'))
            )
            title_input.clear()
            title_input.send_keys('离线请留言')


            # 作为草稿， 后续人工补充图片等
            publish_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="js_submit"]/button'))
            )
            publish_button.click()
        except TimeoutException:
            print('操作超时，请检查元素选择器是否正确')

