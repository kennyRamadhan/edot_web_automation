# config/webdriver_manager.py
import threading

class WebDriverManager:
    _driver = threading.local()

    @classmethod
    def init_driver(cls, factory):
        if not hasattr(cls._driver, "instance") or cls._driver.instance is None:
            cls._driver.instance = factory.create_driver()

    @classmethod
    def get_driver(cls):
        return getattr(cls._driver, "instance", None)

    @classmethod
    def quit_driver(cls):
        driver = getattr(cls._driver, "instance", None)
        if driver:
            driver.quit()
            cls._driver.instance = None
