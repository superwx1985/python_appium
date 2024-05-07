import pytest
import time
import datetime
from os import path
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


app_package = "com.greenworks.tools"
app_activity = "crc64b7a660292f5c8d3e.MainActivity"
email = f'{time.time()}@outlook.com'
screenshot_path = 'screenshot/'

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage="com.google.android.apps.nexuslauncher",
    appActivity=".NexusLauncherActivity",
    noReset=True,  # 启动时不清除app数据
    # language='EN',
    # locale='US',
    udid='emulator-5554',
)


additional_settings = {
    "enforceXPath1": True,
}


appium_server_url = 'http://localhost:4723'


class TestAppium:
    def setup_class(self) -> None:
        dr = self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        dr.update_settings(additional_settings)
        dr.implicitly_wait(30)
        dr.terminate_app(f'{app_package}')
        time.sleep(1)
        dr.activate_app(f'{app_package}/{app_activity}')
        time.sleep(5)

    def teardown_class(self) -> None:
        # self.driver.terminate_app(f'{app_package}')
        if self.driver:
            self.driver.quit()

    def test_creat_account(self) -> None:
        dr = self.driver
        dr.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='yaat-btn-create_account').click()
        time.sleep(2)
        # create account page
        dr.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Name"]/following::android.view.ViewGroup[2]/android.widget.EditText').send_keys('vic')
        dr.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Email*"]/following::android.view.ViewGroup[2]/android.widget.EditText').send_keys(email)
        dr.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Password*"]/following::android.view.ViewGroup[2]/android.widget.EditText').send_keys('Glb123456')
        dr.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Repeat password*"]/following::android.view.ViewGroup[2]/android.widget.EditText').send_keys('Glb123456')
        dr.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Country*"]/following::android.view.ViewGroup[2]/android.widget.Button').click()
        time.sleep(1)
        dr.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Select Region"]/following::android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.EditText').send_keys('united states')
        time.sleep(1)
        dr.find_element(by=AppiumBy.XPATH, value='//androidx.recyclerview.widget.RecyclerView//android.widget.TextView[@text="United States"]').click()
        dr.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@text="NEXT"]').click()
        time.sleep(5)
        # consent page 1
        dr.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='uri-btn-skip').click()
        time.sleep(2)
        dr.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="uri-switch-desc"]/following::android.view.ViewGroup[1]').click()
        time.sleep(1)
        dr.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='uri-btn-next').click()
        time.sleep(2)
        # consent page 2
        x = dr.get_window_size()['width']
        y = dr.get_window_size()['height']
        dr.swipe(x / 2, y / 2, x / 2, y / 4)
        dr.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="uc-switch-desc"]/following::android.view.ViewGroup[1]').click()
        time.sleep(1)
        dr.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='uc-btn-next').click()
        # EULA page
        dr.find_element(by=AppiumBy.CLASS_NAME, value='android.widget.ImageView').click()
        time.sleep(2)
        dr.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="End user license agreement"]/following::android.widget.FrameLayout[1]/android.widget.ScrollView//android.view.ViewGroup/android.widget.TextView/following::android.view.ViewGroup[1]').click()
        time.sleep(1)
        dr.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@text="CREATE ACCOUNT"]').click()
        time.sleep(5)
        assert dr.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Soon friends!"]')
        dr.save_screenshot(path.join(screenshot_path, f"{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.png"))


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-m smoke or debug'])
