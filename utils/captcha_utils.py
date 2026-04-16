import io
from PIL import Image
from playwright.sync_api import Page
from utils.log_utils import logger

def get_slider_gap(page: Page, captcha_img_locator: str) -> int:
    """
    列像素差分识别缺口
    原理：计算列间像素差值总和，最大突变列即为缺口边缘，抗背景干扰极强
    """
    elem = page.locator(captcha_img_locator)
    elem.wait_for(timeout=3000)
    img = Image.open(io.BytesIO(elem.screenshot())).convert("L")
    w, h = img.height, img.width
    diff_list = []

    # 计算每一列与前一列的像素差值总和
    for x in range(80, h - 60):
        diff = 0
        for y in range(int(w*0.2), int(w*0.8)):
            diff += abs(img.getpixel((x, y)) - img.getpixel((x-1, y)))
        diff_list.append((x, diff))

    # 取差值最大的列作为缺口边缘
    diff_list.sort(key=lambda k: k[1], reverse=True)
    gap_x = diff_list[0][0]

    # 偏移校准
    offset = gap_x - 14
    logger.info(f"缺口定位：{gap_x}px，拖动距离：{offset}px")
    return offset

def drag_slider_human(page: Page, slider_locator: str, target_x: int):
    """原生API拖动滑块"""
    slider = page.locator(slider_locator)
    slider.wait_for(state="visible", timeout=3000)

    slider.drag_to(
        slider,
        target_position={"x": target_x, "y": 0},
        force=True
    )
    page.wait_for_timeout(800)
    logger.info("滑块拖动完成")