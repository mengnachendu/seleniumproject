import selenium
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pytest

'''读取yaml文件的数据'''
def get_logindata():
    with open("./data/login_ceshiren.yml") as f:
        data = yaml.safe_load(f)
        ids = []
        list_1 = []
        for row in data['login']:
            ids.append(row[0])
            list_1.append(row[1:3:])
        return [list_1,ids]

#
# if __name__ == '__main__':
#     get_logindata()

class TestCeshiren():

    '''资源准备：打开浏览器、最大化窗口，设置隐式等待时间'''
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://ceshiren.com/latest")
        self.driver.implicitly_wait(5)

    '''资源释放：关闭浏览器'''
    def teardown(self):
        self.driver.quit()

    '''登录测试人网页'''
    def login_ceshiren(self,username,password):
        self.driver.find_element(By.CSS_SELECTOR, ".btn-icon-text .d-button-label").click()
        self.driver.find_element(By.ID, "login-account-name").click()
        self.driver.find_element(By.ID, "login-account-name").send_keys(username)
        self.driver.find_element(By.ID, "login-account-password").click()
        self.driver.find_element(By.ID, "login-account-password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary.btn-icon-text.btn-large .d-button-label").click()
        sleep(3)

    '''测试用例test_demo1'''
    @pytest.mark.parametrize("username,password",get_logindata()[0],ids=get_logindata()[1])
    def test_demo1(self,username,password):

        #1、调用登录函数
        self.login_ceshiren(username,password)

        #2、点击”所有类别“大选择框,点击”就业班“小选择框
        # self.driver.find_element(By.CSS_SELECTOR, ".select-kit-header-wrapper").click()
        self.driver.find_element(By.CSS_SELECTOR, ".category-breadcrumb.ember-view li:nth-of-type(1)").click()
        self.driver.find_element(By.CSS_SELECTOR, ".select-kit-body.ember-view li:nth-of-type(13)").click()

        #3、点击”所有标签“大选择框,点击”就业班“小选择框
        self.driver.find_element(By.CSS_SELECTOR, ".category-breadcrumb.ember-view li:nth-of-type(2)").click()
        # self.driver.find_element(By.CSS_SELECTOR, ".select-kit-collection li:nth-of-type(2)").click()
        self.driver.find_element(By.CSS_SELECTOR, "[data-name='就业班-3期']").click()

        sleep(1)
        #断言
        element = self.driver.find_element(By.CSS_SELECTOR, ".topic-list-body tr:nth-of-type(10) .link-top-line")
        assert "02-27 开班典礼" == element.text




