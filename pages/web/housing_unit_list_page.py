# 新增操作
import allure
from playwright.sync_api import Page, expect
from utils.log_utils import logger

class HousingUnitFormPage:
    def __init__(self, page: Page):
        self.page = page
        # 元素定位器
        self.form_title = page.get_by_role("heading", name="新增房屋单元")
        self.building_select = page.locator("label:has-text('楼栋') + .el-select")
        self.unit_input = page.get_by_placeholder("请输入单元号")
        self.room_input = page.get_by_placeholder("请输入房号")
        self.built_area_input = page.get_by_placeholder("请输入建筑面积")
        self.inner_area_input = page.get_by_placeholder("请输入套内面积")
        self.house_type_select = page.locator("label:has-text('房屋类型') + .el-select")
        self.delivery_status_select = page.locator("label:has-text('交房状态') + .el-select")
        self.save_button = page.get_by_role("button", name="保存")
        self.loading_mask = page.locator(".el-loading-mask")
        self.success_msg = page.get_by_text("提交成功")

    @allure.step("验证进入新增表单页")
    def verify_form_page(self):
        """验证当前页面是新增表单页"""
        expect(self.form_title).to_be_visible()
        allure.attach(self.page.screenshot(), name="新增房屋单元表单", attachment_type=allure.attachment_type.PNG)

    @allure.step("填写新增房屋单元表单")
    def fill_form(self, test_data: dict):
        """填写表单所有字段"""
        logger.info("填写新增房屋单元表单")
        # 选择楼栋
        self.building_select.click()
        self.page.get_by_text(test_data["楼栋"]).click()
        expect(self.building_select).to_have_text(test_data["楼栋"])

        # 输入单元号
        self.unit_input.fill(test_data["单元号"])
        expect(self.unit_input).to_have_value(test_data["单元号"])

        # 输入房号
        self.room_input.fill(test_data["房号"])
        expect(self.room_input).to_have_value(test_data["房号"])

        # 输入建筑面积
        self.built_area_input.fill(test_data["建筑面积"])
        expect(self.built_area_input).to_have_value(test_data["建筑面积"])

        # 输入套内面积
        self.inner_area_input.fill(test_data["套内面积"])
        expect(self.inner_area_input).to_have_value(test_data["套内面积"])

        # 选择房屋类型
        self.house_type_select.click()
        self.page.get_by_text(test_data["房屋类型"]).click()
        expect(self.house_type_select).to_have_text(test_data["房屋类型"])

        # 选择交房状态
        self.delivery_status_select.click()
        self.page.get_by_text(test_data["交房状态"]).click()
        expect(self.delivery_status_select).to_have_text(test_data["交房状态"])

        logger.info("✅ 表单字段填写完毕")
        allure.attach(self.page.screenshot(), name="表单填写完成", attachment_type=allure.attachment_type.PNG)

    @allure.step("点击【保存】按钮提交表单")
    def click_save(self):
        """点击保存按钮提交表单"""
        logger.info("点击【保存】按钮提交表单")
        expect(self.save_button).to_be_enabled()
        self.save_button.click()
        # 等待提交完成，隐藏加载动画
        self.loading_mask.wait_for(state="hidden", timeout=10000)
        logger.info("✅ 表单提交操作完成")

    @allure.step("验证提交成功")
    def verify_submit_success(self, test_url: str, test_data: dict):
        """验证提交成功，新单元出现在列表"""
        logger.info("验证提交成功")
        # 断言成功提示可见
        expect(self.success_msg).to_be_visible(timeout=5000)
        logger.info(f"✅ 成功提示显示：提交成功")

        # 断言返回列表页
        expect(self.page.url).to_contain(f"{test_url}/housing-units", timeout=10000)
        logger.info("✅ 成功返回房屋单元列表页")

        # 断言新单元存在且数据一致
        new_unit_row = self.page.get_by_role("row", name=test_data["房号"])
        expect(new_unit_row).to_be_visible()
        expect(new_unit_row.get_by_text(test_data["楼栋"])).to_be_visible()
        expect(new_unit_row.get_by_text(test_data["单元号"])).to_be_visible()
        expect(new_unit_row.get_by_text(test_data["建筑面积"])).to_be_visible()
        expect(new_unit_row.get_by_text(test_data["房屋类型"])).to_be_visible()
        expect(new_unit_row.get_by_text(test_data["交房状态"])).to_be_visible()
        logger.info(f"✅ 新单元【{test_data['房号']}】已成功添加到列表，数据验证通过")

        allure.attach(self.page.screenshot(), name="提交成功后列表页", attachment_type=allure.attachment_type.PNG)