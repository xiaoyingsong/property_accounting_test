import io
from PIL import Image
from playwright.sync_api import Page
from utils.log_utils import logger


def get_slider_gap(page: Page, captcha_img_locator: str) -> int:
    """
    滑块验证码缺口识别
    基于灰度图查找阴影最暗列，定位缺口位置
    """
    elem = page.locator(captcha_img_locator)
    elem.wait_for(timeout=3000)
    img = Image.open(io.BytesIO(elem.screenshot())).convert("L")
    w, h = img.size

    start_x = 60
    gap_x = 0
    min_brightness = 255

    # 遍历像素查找缺口阴影
    for x in range(start_x, w - 60):
        brightness = 0
        for y in range(int(h * 0.2), int(h * 0.8)):
            brightness += img.getpixel((x, y))
        avg = brightness // 100
        if avg < min_brightness:
            min_brightness = avg
            gap_x = x

    logger.info(f"缺口识别完成，位置：{gap_x} px")
    return gap_x


def drag_slider_human(page: Page, slider_locator: str, target_x: int):
    """
    原生API拖动滑块
    触发前端验证逻辑，精准对齐缺口
    """
    slider = page.locator(slider_locator)
    slider.wait_for(state="visible", timeout=3000)

    # 水平拖动指定距离
    slider.drag_to(
        slider,
        target_position={"x": target_x, "y": 0},
        force=True
    )

    page.wait_for_timeout(800)
    logger.info(f"滑块拖动完成，距离：{target_x} px")