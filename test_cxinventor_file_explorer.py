import pytest
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',  # 可以随便写
    appPackage="com.cxinventor.file.explorer",
    appActivity="com.alphainventor.filemanager.activity.MainActivity",
    noReset=True,  # 启动时不清除app数据
    # language='EN',
    # locale='US',
    # udid='dc289c11'
    udid='127.0.0.1:62001'
)


appium_server_url = 'http://localhost:4723'


class TestAppium:
    def setup_class(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        self.driver.implicitly_wait(5)

    def teardown_class(self) -> None:
        if self.driver:
            self.driver.quit()

    # @pytest.mark.debug
    # @pytest.mark.skip(reason="skip test")
    @pytest.mark.run(order=1)
    def test_confirm_permission(self) -> None:
        text_el_1 = self.driver.find_element(
            AppiumBy.XPATH,
            value='//android.widget.RelativeLayout[@resource-id="com.cxinventor.file.explorer:id/layout_step1"]'
                  '//android.widget.TextView')
        assert "CX文件管理器" == text_el_1.text
        el1 = self.driver.find_element(by=AppiumBy.ID, value='com.cxinventor.file.explorer:id/step1_next')
        el1.click()
        text_el_2 = self.driver.find_element(
            AppiumBy.XPATH,
            value='//android.widget.RelativeLayout[@resource-id="com.cxinventor.file.explorer:id/layout_step2"]'
                  '//android.widget.TextView[1]')
        assert "访问权限请求" == text_el_2.text

        el2 = self.driver.find_element(by=AppiumBy.ID, value='com.cxinventor.file.explorer:id/step2_next')
        el2.click()
        assert "要允许CX文件管理器访问您设备上的照片、媒体内容和文件吗？" == \
               self.driver.find_element(by=AppiumBy.ID, value='com.android.packageinstaller:id/permission_message').text
        self.driver.find_element(by=AppiumBy.ID, value='com.android.packageinstaller:id/permission_allow_button').click()
        assert self.driver.find_element(by=AppiumBy.ID, value='com.cxinventor.file.explorer:id/location_name')

    @pytest.mark.debug
    # @pytest.mark.skip(reason="skip test")
    @pytest.mark.run(order=1)
    def test_debug(self) -> None:
        time.sleep(10)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-m smoke or debug'])
