#处理cookie生成
from config import *
from db import AccountRedisClient,CookieRedisClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from hacker import ManualCaptchaHacker

import requests
import logging,json

logging.basicConfig(level=logging.DEBUG)
class CookieGenerator(object):
    def __init__(self,name='default',browser_type=BROWSER_TYPE):
        self.name = name
        self._account_db = AccountRedisClient(name=self.name)
        self._cookie_db = CookieRedisClient(name=self.name)
        self._browser_type = browser_type
        # self._init_browser()
        self.captchar_hacker = ManualCaptchaHacker()

    #初始化浏览器
    def _init_browser(self):
        if self._browser_type == 'PhantomJS':
            self.browser = webdriver.PhantomJS()
        else:
            self.browser = webdriver.Chrome()


    #根据用户名密码登录，获取cookie
    def gen_cookie(self,username,password):
        raise NotImplementedError


    #获取所有没有cookie的账号，获取cookie
    def run(self):
        accounts = self._account_db.all()
        cookies = self._cookie_db.all()

        if accounts:
            account_list = list(accounts)
            logging.debug('获取了{}个账户'.format(len(account_list)))
            self._init_browser()
            valid_users = [x['username'] for x in cookies]

            for account in account_list:
                if  not account['username']  in valid_users:
                    cookies = self.gen_cookie(account['username'],account['password'])
                    if cookies:
                        logging.debug('生成{}的cookie成功'.format(account['username']))
                        logging.debug('saving cookie to redis {0}'.format(cookies))
                        self._cookie_db.set(account['username'],cookies)
                    else:
                        logging.debug('生成{}的cookie失败'.format(account['username']))
            self.close()

    def close(self):
        if self.browser:
            self.browser.close()

class WeiboCookieGenerator(CookieGenerator):

    def __init__(self,name='weibo',browser_type=BROWSER_TYPE):
        super().__init__(name,browser_type)

    def gen_cookie(self,username,password):

        print('generator cookie:'+username)
        self.browser.delete_all_cookies()
        self.browser.get('http://my.sina.com.cn/profile/unlogin')
        wait = WebDriverWait(self.browser,20)
        btn_go_login = wait.until(EC.element_to_be_clickable((By.ID,'hd_login')))
        btn_go_login.click()
        input_username = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.loginformlist input[name="loginname"]')))
        input_username.clear()
        input_username.send_keys(username)
        input_password = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.loginformlist input[name="password"]')))
        input_password.clear()
        input_password.send_keys(password)

        btn_login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.login_btn')))
        btn_login.click()

        try:

            result = self._success()
            if result:
                return result

        except TimeoutException:
            print('登录失败')


            #处理验证码
            yzm = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'li.loginform_yzm > img.yzm')))
            yzm_src = yzm.get_attribute('src')
            if yzm_src:

                #需要携带cookie
                cookies = self.browser.get_cookies()
                cookie_dict = {}

                for c in cookies:
                    cookie_dict[c.get('name')]=c.get('value')

                response = requests.get(yzm_src,cookies=cookie_dict)
                if response.status_code == 200:
                    captcha = self.captchar_hacker.resolve(response.content)
                    if captcha:
                        print('得到了验证码',captcha)
                        yzm_input = self.browser.find_element_by_css_selector('li.loginform_yzm > input')
                        yzm_input.clear()
                        yzm_input.send_keys(captcha)
                        btn_login.click()
                        result = self._success()
                        if result:
                            return result


    def _success(self):
        wait = WebDriverWait(self.browser, 10)
        portrait = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.me_portrait')))
        if portrait:
            print('登录成功')
            self.browser.get('http://weibo.cn/')
            cookies = self.browser.get_cookies()
            cookie_dict = {}
            for c in cookies:
                cookie_dict[c.get('name')] = c.get('value')
            return json.dumps(cookie_dict)

if __name__ == '__main__':
    wcg  = WeiboCookieGenerator()
    wcg.run()