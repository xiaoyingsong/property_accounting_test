import io
import random
from PIL import Image, ImageFilter
from playwright.sync_api import Page
from utils.log_utils import logger

def _collect_gap_candidates(page: Page, captcha_img_locator: str):
    """
    基于边缘投影 + 双峰配对识别滑块缺口。
    1) 先对图像做轻微高斯平滑降噪
    2) 计算每列横向梯度强度（缺口边缘会形成高响应）
    3) 在候选峰中寻找“左右边缘成对”的最佳组合
    """
    elem = page.locator(captcha_img_locator)
    elem.wait_for(timeout=3000)
    img = Image.open(io.BytesIO(elem.screenshot())).convert("L").filter(ImageFilter.GaussianBlur(1))
    width, height = img.size
    pixels = img.load()

    y_start = int(height * 0.2)
    y_end = int(height * 0.85)
    col_score = [0.0 for _ in range(width)]

    # 计算每列横向梯度强度（仅在有效高度范围内）
    for x in range(1, width - 1):
        score = 0
        for y in range(y_start, y_end):
            left_grad = abs(pixels[x, y] - pixels[x - 1, y])
            right_grad = abs(pixels[x + 1, y] - pixels[x, y])
            score += left_grad + right_grad
        col_score[x] = score / max(1, (y_end - y_start))

    # 移动平均平滑，减少随机噪声峰
    smooth = [0.0 for _ in range(width)]
    radius = 3
    for x in range(radius, width - radius):
        smooth[x] = sum(col_score[x - radius:x + radius + 1]) / (2 * radius + 1)

    # 候选峰：局部极大 + 排除边缘区域
    candidates = []
    # 经验上左侧装饰干扰较重，收紧搜索范围
    min_x, max_x = int(width * 0.2), width - 45
    for x in range(min_x, max_x):
        if smooth[x] > smooth[x - 1] and smooth[x] >= smooth[x + 1]:
            candidates.append((x, smooth[x]))

    if not candidates:
        # 极端情况下回退
        gap_x = max(range(min_x, max_x), key=lambda i: smooth[i])
        return [(gap_x, 0.0, "fallback")]

    candidates.sort(key=lambda kv: kv[1], reverse=True)
    top_candidates = candidates[:30]

    # 缺口通常会出现左右两条边缘，宽度在一个范围内
    pair_scores = []
    expected_gap_width = 48
    min_gap_width = 30
    max_gap_width = 72

    for lx, lv in top_candidates:
        for rx, rv in top_candidates:
            if rx <= lx:
                continue
            gap_width = rx - lx
            if not (min_gap_width <= gap_width <= max_gap_width):
                continue
            width_penalty = abs(gap_width - expected_gap_width) * 1.8
            pair_score = (lv + rv) - width_penalty
            pair_scores.append((pair_score, lx, gap_width))

    if pair_scores:
        pair_scores.sort(key=lambda t: t[0], reverse=True)
        best_score = pair_scores[0][0]
        out = []
        used_x = set()
        for score, lx, gap_width in pair_scores:
            if len(out) >= 4:
                break
            # 去重：相近位置只留一个
            if any(abs(lx - ux) <= 8 for ux in used_x):
                continue
            conf = score / best_score if best_score > 0 else 0.0
            out.append((lx, conf, f"pair(width={gap_width})"))
            used_x.add(lx)
        return out

    # 无配对结果时回退到单峰
    return [(top_candidates[0][0], 0.0, "single-peak")]


def get_slider_gap(page: Page, captcha_img_locator: str) -> int:
    """
    返回首选缺口偏移，兼容旧调用。
    """
    gap_x, _conf, method = _collect_gap_candidates(page, captcha_img_locator)[0]
    offset = gap_x - 14
    logger.info(f"缺口定位：{gap_x}px，拖动距离：{offset}px，识别方式：{method}")
    return offset


def get_slider_gap_candidates(page: Page, captcha_img_locator: str):
    """
    返回多个候选偏移，供外层重试策略逐个尝试。
    """
    raw_candidates = _collect_gap_candidates(page, captcha_img_locator)
    offsets = []
    for gap_x, conf, method in raw_candidates:
        offset = max(1, gap_x - 14)
        offsets.append((offset, conf, method))
    logger.info(
        "滑块候选偏移: "
        + ", ".join([f"{off}px(conf={conf:.2f},{m})" for off, conf, m in offsets])
    )
    return offsets

def drag_slider_human(page: Page, slider_locator: str, target_x: int):
    """模拟人类鼠标轨迹拖动滑块"""
    slider = page.locator(slider_locator)
    slider.wait_for(state="visible", timeout=3000)
    box = slider.bounding_box()
    if not box:
        raise RuntimeError("滑块元素不可见，无法获取坐标")

    start_x = box["x"] + box["width"] / 2
    start_y = box["y"] + box["height"] / 2
    end_x = start_x + max(1, target_x)

    page.mouse.move(start_x, start_y)
    page.mouse.down()

    # 分段拖动并加入轻微抖动，降低被识别为机器轨迹的概率
    steps = max(12, min(30, int(abs(target_x) / 8)))
    for i in range(1, steps + 1):
        progress = i / steps
        jitter_y = random.uniform(-1.5, 1.5)
        current_x = start_x + (end_x - start_x) * progress
        page.mouse.move(current_x, start_y + jitter_y)
        page.wait_for_timeout(random.randint(8, 24))

    page.wait_for_timeout(random.randint(60, 140))
    page.mouse.up()
    page.wait_for_timeout(900)
    logger.info("滑块拖动完成")