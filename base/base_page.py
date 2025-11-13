from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import allure
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def safe_click(self, element, timeout=10):

        try:
            # tunggu element muncul dan clickable
            el = WebDriverWait(self.driver, timeout).until(
                lambda d: element if element.is_displayed() and element.is_enabled() else False
            )

            # scroll ke center viewport
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

            # coba JS click
            try:
                self.driver.execute_script("arguments[0].click();", el)
            except ElementClickInterceptedException:
                # fallback ke ActionChains
                actions = ActionChains(self.driver)
                actions.move_to_element(el).pause(0.2).click().perform()

        except StaleElementReferenceException:
            # kalau element hilang karena rerender, bisa retry sekali
            el = WebDriverWait(self.driver, timeout).until(
                lambda d: element if element.is_displayed() and element.is_enabled() else False
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            try:
                self.driver.execute_script("arguments[0].click();", el)
            except:
                actions = ActionChains(self.driver)
                actions.move_to_element(el).pause(0.2).click().perform()

    def find_element(self, by, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
        EC.visibility_of_element_located((by, locator))
    )
    def find_elements(self, by, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
        EC.presence_of_all_elements_located((by, locator))
    )

    def take_screenshot(self, name="screenshot"):
        # Ambil screenshot dan simpan sebagai bytes
        screenshot = self.driver.get_screenshot_as_png()
        # Attach ke Allure report
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)

    
    def click(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def type_text(self, locator, text, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)

    def get_text(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element.text

    def is_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False
    

    def wait_until_visible(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_until_present(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_until_clickable(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_until_disappear(self, locator, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def wait_until_text_present(self, locator, text, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
