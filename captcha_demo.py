# !/usr/bin/python3
# -*- coding:utf-8 -*- 

import re
from io import BytesIO
import random
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import requests


def get_image(driver, path):
    """
    下载验证码图片和全部图片的偏移值。
    :param driver: webdriver实例
    :param path: 图片的xpath路径
    :return: 验证码图片，全部图片偏移值的列表
    """
    image_list = driver.find_elements_by_xpath(path)
    location_list = []
    for img in image_list:
        result = re.findall(r'url\("(.*?)"\); background-position: (.*?)px (.*?)px', img.get_attribute('style'))[0]
        location = {}
        location['x'] = int(result[1])
        location['y'] = int(result[2])
        location_list.append(location)
        image_url = result[0]

    image_url = image_url.replace('webp', 'jpg')
    image_result = requests.get(image_url).content
    image_file = BytesIO(image_result)

    image = merge_image(image_file, location_list)
    return image


def merge_image(image_file, location_list):
    """
    把无序的图片切割成小份，再按偏移值拼接成正确的图片。
    :param image_file: 无序验证码图片
    :param location_list: 偏移值列表
    :return: 正确的验证码图片
    """
    image = Image.open(image_file)
    new_image = Image.new('RGB', (260, 116))

    image_list_up = []
    image_list_down = []
    for location in location_list:
        if location['y'] == -58:
            image_list_up.append(image.crop((abs(location['x']), 58, abs(location['x'])+10, 116)))
        if location['y'] == 0:
            image_list_down.append(image.crop((abs(location['x']), 0, abs(location['x'])+10, 58)))

    x_offset = 0
    for img in image_list_up:
        new_image.paste(img, (x_offset, 0))
        x_offset += img.size[0]

    x_offset = 0
    for img in image_list_down:
        new_image.paste(img, (x_offset, 58))
        x_offset += img.size[0]
    return new_image


def is_gap(image1, image2, x, y):
    """
    比较两张图片在某个坐标点的像素，如果像素差距大于45，返回False；否则返回True
    :param image1: 图片1
    :param image2: 图片2
    :param x: x坐标
    :param y: y坐标
    :return: True or False
    """
    pixel1 = image1.getpixel((x, y))
    pixel2 = image2.getpixel((x, y))
    for i in range(3):
        if abs(pixel1[i] - pixel2[i]) > 45:
            return False
    return True


def get_gap_location(image1, image2):
    """
    获取滑动验证码缺口的x坐标
    :param image1: 完整的验证码图片
    :param image2: 有缺口的验证码图片
    :return:
    """
    for x in range(259, 0, -1):
        for y in range(116):
            if not is_gap(image1, image2, x, y):
                return x


def simulation_drag(length):
    """
    模拟人拖动滑动验证码的过程
    :param length: 滑动验证码缺口的x坐标
    :return: 位移距离的列表
    """
    move_list = []
    current_place, slow_place, t, v = 0, length * 3/5, 0.1, 0
    while current_place < length:
        a = random.uniform(2.2, 2.4) if current_place < slow_place else random.uniform(1.6, 1.8)
        v0 = v
        v = v0 + a * t
        move_distance = v0 * t + 0.5 * a * t**2
        current_place += move_distance
        move_list.append(round(move_distance, 4))

    move_list.extend([-1 for i in range(3)])
    return move_list


def main(driver):
    driver.get('http://www.cnbaowen.net/api/geetest/')

    element = WebDriverWait(driver, 60, 0.5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'gt_slider_knob')))
    image1 = get_image(driver, '//*[@id="captcha"]/div/div[1]/div[2]/div[1]/a[2]/div[1]/div')
    image2 = get_image(driver, '//*[@id="captcha"]/div/div[1]/div[2]/div[1]/a[1]/div[1]/div')
    length = get_gap_location(image1, image2)
    move_list = simulation_drag(length)

    ActionChains(driver).click_and_hold(on_element=element).perform()
    time.sleep(0.5)
    for move in move_list:
        ActionChains(driver).move_by_offset(xoffset=move, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=-1, yoffset=0).perform()
    time.sleep(0.3)
    ActionChains(driver).release(on_element=element).perform()
    time.sleep(10)


if __name__ == '__main__':
    try:
        driver = webdriver.Chrome()
        main(driver)
    finally:
        driver.close()
