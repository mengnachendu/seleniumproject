import yaml
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from faker import Faker
from qiyeweixin.utils_tool.logging_info import logger
from qiyeweixin.utils_tool.web_utils import click_exception_user_defined
import datetime
import allure
import pytest
from selenium.webdriver.support.wait import WebDriverWait


class TestQiYeWeiXin:

    #前置动作
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(3)

        self.driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx")
        cookies = yaml.safe_load(open("../data/qiyeweixin_cookie.yaml"))
        for i in cookies:
            self.driver.add_cookie(i)

    #后置动作
    def teardown_class(self):
        self.driver.quit()

    def exception_handle(func):
        def inner(*args, **kwargs):
            try:
                driver = args[0].driver
                func(*args, **kwargs)
            except:
                strstamp = datetime.datetime.now()
                fmt_time = strstamp.strftime("%Y%m%d_%H%M%S")

                #定义异常截图存放路径，并进行截图操作
                image_path = f"../image/image_{fmt_time}.png"
                driver.save_screenshot(image_path)

                #定义异常源码存放路径，并把异常源码保存到文件中
                page_source_path = f"../page_source/page_source_{fmt_time}.html"
                with open(page_source_path, 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)

                #把异常截图、源码写入到测试报告中
                logger.info("这里出现异常了")
                allure.attach.file(image_path, "异常截图", attachment_type=allure.attachment_type.PNG)
                allure.attach.file(page_source_path, "异常源码", attachment_type=allure.attachment_type.TEXT)

                raise Exception
        return inner

    #获取cookie并保存到文件中
    @pytest.mark.skip
    def test_get_cookie(self):
        self.driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx")
        sleep(15)
        cookie = self.driver.get_cookies()
        with open("../data/qiyeweixin_cookie.yaml", 'w', encoding='utf-8') as f:
            yaml.safe_dump(cookie, f)

    #case1：在首页菜单:点击添加成员按钮后，添加成员
    @exception_handle
    def test_add_member_1(self):

        #设置随机数
        fake = Faker("zh_CN")
        self.username = fake.name()
        self.acctid = fake.ssn()
        self.mobile = fake.phone_number()
        self.mail = fake.postcode()

        #1、登录页面：登录
        logger.info("1、登录页面：登录")
        self.driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx")

        #2、首页：点击添加成员按钮
        logger.info("2、首页：点击添加成员菜单")
        self.driver.find_element(By.XPATH, "//*[text()='添加成员']").click()

        # 3、添加成员信息页面：输入成员个人信息后保存
        logger.info("3、成员信息页面：输入成员个人信息后保存")
        self.driver.find_element(By.NAME, "username").send_keys(self.username)
        self.driver.find_element(By.ID, "memberAdd_acctid").send_keys(self.acctid)
        self.driver.find_element(By.ID, "memberAdd_biz_mail").clear()
        self.driver.find_element(By.ID, "memberAdd_biz_mail").send_keys(self.mail)
        self.driver.find_element(By.ID, "memberAdd_phone").send_keys(self.mobile)
        self.driver.find_element(By.XPATH, "//*[text()='保存']").click()

        # 4、成员列表页面：断言添加操作的测试结果
        logger.info("4、成员列表页面：断言添加操作的测试结果")
        ele = self.driver.find_element(By.ID, "js_tips")
        add_msg = ele.text
        assert "保存成功" == add_msg

        #5、清楚脏数据，成员信息页面：选中指定的成员后删除
        logger.info("5、成员信息页面：选中指定的成员后删除")
        self.driver.find_element(By.XPATH, f"//*[text()='{self.username}']/../..//*[@class='ww_checkbox1']").click()
        self.driver.find_element(By.XPATH, "//*[@class='ww_operationBar']//*[text()='删除']").click()
        self.driver.find_element(By.XPATH, "//*[text()='确认']").click()

        # 6、成员信息页面：断言删除操作的测试结果
        logger.info("6、成员信息页面：断言删除操作的测试结果")
        ele1 = self.driver.find_element(By.XPATH, "//*[text()='删除成功']")
        del_result = ele1.text
        assert "删除成功" == del_result

    #case2：在通讯录菜单：点击添加成员按钮，添加成员
    def test_add_member_2(self):

        #设置随机数
        fake = Faker("zh_CN")
        self.username = fake.name()
        self.acctid = fake.ssn()
        self.mobile = fake.phone_number()

        # 1、登录页面：登录
        logger.info("1、登录页面：登录")
        self.driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx")

        #2、首页：点击通讯录菜单
        logger.info("2、首页：点击通讯录菜单")
        self.driver.find_element(By.XPATH, "//*[text()='通讯录']").click()

        #3、添加成员列表页面：点击添加成员按键
        logger.info("3、添加成员列表页面：点击添加成员")
        WebDriverWait(self.driver, 10).until(
            click_exception_user_defined(By.XPATH, "//*[text()='添加成员']"))

        # 4、添加成员信息页面：输入成员个人信息后保存
        logger.info("4、添加成员信息页面：输入成员个人信息后保存")
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(
                (By.NAME, "username"))).send_keys(self.username)
        self.driver.find_element(By.ID, "memberAdd_acctid").send_keys(self.acctid)
        self.driver.find_element(By.ID, "memberAdd_biz_mail").clear()
        self.driver.find_element(By.ID, "memberAdd_biz_mail").send_keys(self.mobile)
        self.driver.find_element(By.ID, "memberAdd_phone").send_keys(self.mobile)
        self.driver.find_element(By.XPATH, "//*[text()='保存']").click()

        # 5、成员列表页面：断言添加操作的测试结果
        logger.info("5、成员列表页面：断言添加操作的测试结果")
        ele = self.driver.find_element(By.ID, "js_tips")
        add_msg = ele.text
        assert "保存成功" == add_msg

        #6、清楚脏数据，成员信息页面：选中指定的成员后删除
        logger.info("6、成员列表页面：选中制定的成员后删除")
        self.driver.find_element(By.XPATH, f"//*[text()='{self.username}']/../..//*[@class='ww_checkbox']").click()
        self.driver.find_element(By.XPATH, "//*[@class='ww_operationBar']//*[text()='删除']").click()
        self.driver.find_element(By.XPATH, "//*[text()='确认']").click()

        #7、成员信息页面：断言删除操作的测试结果
        logger.info("7、成员信息页面：断言删除操作的测试结果")
        ele1 = self.driver.find_element(By.XPATH, "//*[text()='删除成功']")
        del_result = ele1.text
        assert "删除成功" == del_result

    #case3：在首页菜单：点击添加部门按钮，添加部门
    def test_add_depart(self):

        # 设置随机数
        fake = Faker("zh_CN")
        self.username = fake.name()
        self.acctid = fake.ssn()
        self.mobile = fake.phone_number()
        self.district = fake.district()

        # 1、登录页面：登录
        logger.info("1、登录页面：登录")
        self.driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx")

        # 2、首页：点击通讯录菜单
        logger.info("2、首页：点击通讯录菜单")
        self.driver.find_element(By.XPATH, "//*[text()='通讯录']").click()

        #3、成员列表页面：点击左侧“+”按钮,然后点击添加部门按钮
        logger.info("3、成员列表页面：点击添加部门按钮")
        self.driver.find_element(By.CSS_SELECTOR, ".member_colLeft_top_addBtn").click()
        self.driver.find_element(By.CSS_SELECTOR, ".js_create_party").click()

        #4、新建部门页面：输入部门名称并选择所属部门后确定
        logger.info("4、新建部门页面：输入部门名称并选择所属部门后确定")
        self.driver.find_element(By.NAME, "name").send_keys(f"{self.district}区")
        #点击所属部门下拉框
        self.driver.find_element(By.XPATH, "//*[text()='选择所属部门']").click()
        #选择对应部门
        self.driver.find_element(By.XPATH, "//*[text()='新建部门']/../../div[2]//li[3]").click()
        #点击确定按钮
        self.driver.find_element(By.XPATH, "//*[text()='确定']").click()

        #5、部门列表页面：断言新增操作的测试结果
        logger.info("5、部门列表页面：断言新增操作的测试结果")
        ele = self.driver.find_element(By.XPATH, "//*[text()='新建部门成功']")
        add_msg = ele.text
        assert "新建部门成功"  == add_msg

        #6、清楚脏数据，部门列表页面：选中制定的部门进行删除
        logger.info("6、部门列表页面：选中制定的部门进行删除")
        self.driver.find_element(By.XPATH, f"//*[text()='{self.district}区']/span").click()
        self.driver.find_element(By.XPATH, "//body/ul//*[text()='删除']").click()
        self.driver.find_element(By.XPATH, "//*[text()='确定']").click()

        #7、部门列表页面：断言删除操作的测试结果
        logger.info("7、部门列表页面：断言删除操作的测试结果")
        ele = self.driver.find_element(By.XPATH, "//*[text()='删除部门成功']")
        del_msg = ele.text
        assert "删除部门成功" == del_msg






