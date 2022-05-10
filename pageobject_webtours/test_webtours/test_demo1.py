import pytest
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from pageobject_webtours.page_objects.login_page import LoginPage
from pageobject_webtours.page_objects.base_page import BasePage

class TestLitemall:
    def setup_class(self):
        self.home = LoginPage().login()
    #
    def teardown_class(self):
        self.home.do_quit()

    # @pytest.mark.parametrize(category_name, ['test1','test2','test3'])
    def test_add_type(self):
        element = self.home\
            .go_to_category()\
            .click_add()\
            .category_create("新增商品测试")\
            .get_create_category_result()

        assert element == "创建成功"

    # @pytest.mark.parametrize(category_name, ['test2'])
    def test_delete_type(self):
        element = self.home\
            .go_to_category()\
            .click_add()\
            .category_create("删除商品测试")\
            .click_delete_category()\
            .get_delete_category_result()

        assert "删除成功" == element


