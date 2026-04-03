import io
import random
from PIL import Image
from playwright.sync_api import Page


def get_slider_gap(page: Page, captcha_img_locator: str) -> int:
    """
    识别滑块验证码的缺口位置，返回缺口的X坐标
    :param page: Playwright Page对象
    :param captcha_img_locator: 验证码图片的定位器（用于精准截图）
    :return: 缺口的X坐标（需拖动的距离）
    """
    # 1. 截取验证码图片
    captcha_img = page.locator(captcha_img_locator).screenshot()
    img = Image.open(io.BytesIO(captcha_img)).convert("RGB")

    # 2. 像素对比找缺口（根据你截图的雪景/建筑背景调整阈值）
    left = 0
    # 遍历图片像素，找明显差异的缺口位置
    for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((x, y))
            # 背景是亮色调，缺口是拼图的深色轮廓，可根据实际图片调整阈值
            if r < 60 and g < 60 and b < 60:
                left = x
                break
        if left > 0:
            break
    # 减去滑块宽度偏移（根据实际滑块大小调整，通常40-50px）
    return left - 45


def drag_slider_human(page: Page, slider_locator: str, gap_x: int):
    """
    模拟人类拖动滑块（带缓动+微小抖动，降低反爬检测）
    :param page: Playwright Page对象
    :param slider_locator: 滑块的定位器
    :param gap_x: 缺口的X坐标（需拖动的距离）
    """
    # 1. 获取滑块初始位置
    slider = page.locator(slider_locator)
    slider_bbox = slider.bounding_box()
    if not slider_bbox:
        raise Exception("滑块元素定位失败")

    # 2. 计算拖动起点/终点
    start_x = slider_bbox["x"] + slider_bbox["width"] / 2
    start_y = slider_bbox["y"] + slider_bbox["height"] / 2
    end_x = start_x + gap_x
    end_y = start_y

    # 3. 模拟人类拖动轨迹：先加速、再匀速、最后减速+微小抖动
    page.mouse.move(start_x, start_y)
    page.mouse.down()
    steps = 20  # 分段数越多，轨迹越自然
    for i in range(1, steps + 1):
        ratio = i / steps
        # 缓动函数（ease-out）：模拟人手先快后慢
        ease_ratio = 1 - (1 - ratio) ** 3
        # 加微小Y轴抖动，模拟人手晃动
        y_offset = 2 * (0.5 - random.random())
        current_x = start_x + (end_x - start_x) * ease_ratio
        current_y = end_y + y_offset
        page.mouse.move(current_x, current_y, steps=1)
    page.mouse.up()
