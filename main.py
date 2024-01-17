import pytest
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage="com.android.launcher3",
    appActivity=".launcher3.Launcher",
    # language='EN',
    # locale='US',
    # udid='dc289c11'
    udid='127.0.0.1:62001'
)


appium_server_url = 'http://localhost:4723'


class TestAppium:
    def setup_class(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def teardown_class(self) -> None:
        if self.driver:
            self.driver.quit()

    # @pytest.mark.debug
    # @pytest.mark.skip(reason="skip test")
    @pytest.mark.run(order=1)
    def test_find_WLAN(self) -> None:
        package_name = "com.android.settings"
        activity_name = ".Settings"
        self.driver.activate_app(f'{package_name}/{activity_name}')
        assert activity_name == self.driver.current_activity
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="WLAN"]')
        el.click()
        time.sleep(2)
        assert ".Settings$WifiSettingsActivity" == self.driver.current_activity

    @pytest.mark.run(order=2)
    def test_switch_another_app(self):
        package_name = "com.android.contacts"
        activity_name = ".activities.PeopleActivity"
        self.driver.activate_app(f'{package_name}/{activity_name}')
        # self.driver.execute_script(
        #     'mobile: startActivity',
        #     {
        #         'component': f'{package_name}/{activity_name}',
        #     },
        # )
        time.sleep(2)
        assert package_name == self.driver.current_package
        assert activity_name == self.driver.current_activity

    @pytest.mark.run(order=3)
    def test_close_app(self):
        self.driver.terminate_app("com.android.settings")
        time.sleep(2)
        assert "com.android.launcher3" == self.driver.current_package

    @pytest.mark.run(order=4)
    def test_install_and_remove_app(self):
        package_name = "com.cxinventor.file.explorer"
        assert not self.driver.is_app_installed(f"{package_name}")
        self.driver.install_app("E:\\Downloads\\Cx File Explorer_2.1.5.apk")
        assert self.driver.is_app_installed(f"{package_name}")
        self.driver.remove_app(f"{package_name}")
        assert not self.driver.is_app_installed(f"{package_name}")

    @pytest.mark.debug
    @pytest.mark.run(order=5)
    def test_background_app(self):
        package_name = "com.android.contacts"
        activity_name = ".activities.PeopleActivity"
        self.driver.activate_app(f'{package_name}/{activity_name}')
        assert activity_name == self.driver.current_activity
        self.driver.background_app(5)
        time.sleep(2)
        # assert ".launcher3.Launcher" == self.driver.current_activity
        # time.sleep(5)
        assert activity_name == self.driver.current_activity


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-m smoke or debug'])
