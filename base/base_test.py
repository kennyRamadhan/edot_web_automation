# base/base_test.py
import pytest
from config.web_driver_manager import WebDriverManager
from config.driver_factory import DriverFactory

class BaseTest:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, request):
        print("\n===== Starting Test Setup =====")
        WebDriverManager.init_driver(DriverFactory())
        self.driver = WebDriverManager.get_driver()
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(120)
        self.driver.implicitly_wait(100)
        

        # Load base URL
        base_url = "https://esuite.edot.id"
        print(f">>> Opening URL: {base_url}")
        self.driver.get(base_url)

        yield  # — menjalankan test case

        print("\n===== Cleaning Up Test =====")
        WebDriverManager.quit_driver()
