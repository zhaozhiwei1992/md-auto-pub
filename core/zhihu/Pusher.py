"""
自定义知乎, Pusher
"""
import os
# import markdown

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from core.AbstractPusher import AbstractPusher

class Pusher(AbstractPusher):

    def getCookiePath(self, rootPath):
        return os.path.abspath(os.path.join(rootPath, 'zhihu_cookie.json'))

    def write(self, driver, config, markdownProperties):
        try:
            # 输入标题
            title_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "title"))
            )
            title_input.clear()
            title_input.send_keys(markdownProperties['title'])

            # 打开新页签， 通过https://md.phodal.com/转换markdown然后获取内容
            # markdownContent = markdownProperties['content']
            # main_window = driver.current_window_handle
            # driver.execute_script("window.open('" + config["TRANS_MD"] + "')")
            # 打开上述网站将markdown内容贴入
            # 复制转换后的内容给content变量
            # content = ""
            # 回到之前页面
            # driver.switch_to.window(main_window)

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

