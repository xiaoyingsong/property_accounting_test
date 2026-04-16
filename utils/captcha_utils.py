import io
from PIL import Image
from playwright.sync_api import Page
from utils.log_utils import logger

def get_slider_gap(page: Page, captcha_img_locator: str) -> int:
    """
    整块阴影区域识别
    原理：查找垂直方向连续暗点 → 真正拼图缺口
    抗干扰极强，适配所有随机背景
    """
    elem = page.locator(captcha_img_locator)
    elem.wait_for(timeout=3000)
    img = Image.open(io.BytesIO(elem.screenshot())).convert("L")
    w, h = img.size

    start_x = 70
    gap_x = 0
    threshold = 100  # 暗点阈值
    require_count = 40  # 垂直连续40个暗点才算缺口（极强抗干扰）

    for x in range(start_x, w - 60):
        count = 0
        for y in range(int(h*0.2), int(h*0.8)):
            if img.getpixel((x, y)) < threshold:
                count += 1
            else:
                count = 0

            if count >= require_count:
                gap_x = x
                logger.info(f"缺口定位：{gap_x}px")
                return gap_x - 12

    logger.info(f" fallback 缺口定位：{w//2}px")
    return w // 2 - 12

def drag_slider_human(page: Page, slider_locator: str, target_x: int):
    """
    原生拖动
    """
    slider = page.locator(slider_locator)
    slider.wait_for(state="visible", timeout=3000)

    slider.drag_to(
        slider,
        target_position={"x": target_x, "y": 0},
        force=True
    )
    page.wait_for_timeout(800)
    logger.info("滑块拖动完成")