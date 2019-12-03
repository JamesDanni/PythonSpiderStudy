# -*- coding: utf-8 -*-

from selenium import webdriver
import time

class MySelenium():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.file = open("url_list.txt", "r")
        self.url_list = self.file.readlines()
        self.file.close()
        self.goods_info_list = []
        self.count = 0

        self.lipstick_brand = ""
        self.lipstick_name = ""
        self.lipstick_desc = ""
        self.lipstick_price = ""
        self.lipstick_img = ""
        self.lipstick_col_list = []
        self.lipstick_product_comment_satisfy_num = ""
        self.c_comment_tag_list_name = []
        self.total_c_comment_tag_list_name = []
        self.total_c_comment_tag_list_name = []

        self.total_buy_color_count_list = []

    def get_tag_list(self,url):
        try:
            self.driver.get(url.strip())
            for i in range(15):
                self.driver.execute_script("window.scrollBy(0,1000);")
                time.sleep(3)
            time.sleep(10)
            self.lipstick_brand = self.driver.find_element_by_xpath("//a[contains(@class,'J_brandName')]").text
            self.lipstick_name = self.driver.find_element_by_xpath("//p[@class='pib-title-detail']").text
            self.lipstick_desc = self.driver.find_element_by_xpath("//span[@class='goods-description-title']").text
            self.lipstick_price = self.driver.find_element_by_xpath(
                "//div[@class='sp-info'] | //div[@class='pb-vipPrice']").text
            self.lipstick_img = self.driver.find_element_by_xpath("//img[@class='slide-mid-pic']").get_attribute("src")
            self.lipstick_col_list = self.driver.find_elements_by_xpath(
                "//dd[@class='color-list']//span[@class='color-item-name']")
            self.lipstick_product_comment_satisfy_num = self.driver.find_element_by_xpath(
                "//span[@class='c-product-comment-satisfy-num']").text
            self.c_comment_tag_list_name = self.driver.find_elements_by_xpath("//div[@class='c-product-comment-tags']//a")
            self.total_c_comment_tag_list_name = []
            for c_comment_tag in self.c_comment_tag_list_name:
                if c_comment_tag.text.find("(") != -1:
                    self.total_c_comment_tag_list_name.append(c_comment_tag.text.replace(" ", ""))
        except:
            pass

    def get_buy_color_count_list(self):
        buy_color_count_list = []
        j = 1
        while j <= 20:
            listick_driver_public_info_size_list = self.driver.find_elements_by_xpath("//span[@class='public-info-size'][1]")
            for listick_driver_public_info_size in listick_driver_public_info_size_list:
                buy_color_count_list.append(listick_driver_public_info_size.text[4:])
            try:
                self.driver.find_element_by_xpath("//a[@id='J_next_paging']").click()
            except:
                pass
            time.sleep(3)
            j += 1
        buy_color_count_set = set(buy_color_count_list)
        self.total_buy_color_count_list = []
        for color in buy_color_count_set:
            dict1 = {color: buy_color_count_list.count(color)}
            self.total_buy_color_count_list.append(dict1)

    def save_data(self):
        for i in self.total_buy_color_count_list:
            self.count += 1
            with open("weipin.txt", "a", encoding="utf8") as file:
                file.write("第" + str(self.count) + "条:" + str(
                    {"口红品牌": self.lipstick_brand, "口红名字": self.lipstick_name, "口红描述": self.lipstick_desc, "口红价格": self.lipstick_price,
                     "口红图片": self.lipstick_img, "口红用户满意度": self.lipstick_product_comment_satisfy_num, "口红销量": str(i),
                     "口红评价": str(self.total_c_comment_tag_list_name)}) + "\n")

if __name__ == '__main__':
    my_selenium = MySelenium()
    for url in my_selenium.url_list:
        my_selenium.get_tag_list(url)
        my_selenium.get_buy_color_count_list()
        my_selenium.save_data()