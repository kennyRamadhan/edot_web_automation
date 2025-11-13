import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)
from selenium.webdriver.common.action_chains import ActionChains

from config.web_driver_manager import WebDriverManager 


class CustomCommand:
    """Kumpulan utilitas umum untuk interaksi Web UI di Selenium Python."""

    DEFAULT_TIMEOUT = 60
    RETRY_COUNT = 3
    SLEEP_MS = 0.3  # dalam detik

    @staticmethod
    def _get_driver_safe():
        """Pastikan driver sudah diinisialisasi sebelum digunakan."""
        driver = WebDriverManager.get_driver()
        if driver is None:
            raise RuntimeError("Driver belum diinisialisasi! Pastikan WebDriverManager.init_driver() sudah dipanggil.")
        return driver


    @staticmethod
    def send_keys_when_ready(element, text):
        driver = CustomCommand._get_driver_safe()
        wait = WebDriverWait(driver, CustomCommand.DEFAULT_TIMEOUT)
        wait.until(EC.visibility_of(element))
        wait.until(EC.element_to_be_clickable(element))
        element.clear()

        if text is None:
            print(f"⚠️ Nilai 'None' diterima untuk elemen {element} — input dilewati.")
            return

        element.send_keys(text)
        print(f" Input text: '{text}' pada elemen: {element}")

    @staticmethod
    def click_when_ready(element):
        driver = CustomCommand._get_driver_safe()
        wait = WebDriverWait(driver, 10)
        for attempt in range(2):
            try:
                wait.until(EC.element_to_be_clickable(element)).click()
                print(" Klik berhasil")
                return
            except StaleElementReferenceException:
                print(" Elemen stale saat klik, mencoba ulang...")

    @staticmethod
    def verify_element_exist(element):
        driver = CustomCommand._get_driver_safe()
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of(element))
            print(f"Element ditemukan: {element}")
        except TimeoutException:
            raise RuntimeError(f" Element tidak ditemukan: {element}")

    @staticmethod
    def is_element_present(element):
        try:
            return element.is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    @staticmethod
    def verify_element_not_exist(by: By):
        driver = CustomCommand._get_driver_safe()
        try:
            invisible = WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(by))
            if invisible:
                print(f"Element tidak ditemukan (expected): {by}")
        except TimeoutException:
            raise RuntimeError(f"Element masih muncul padahal seharusnya tidak: {by}")


    @staticmethod
    def get_text_when_ready(element):
        driver = CustomCommand._get_driver_safe()
        WebDriverWait(driver, CustomCommand.DEFAULT_TIMEOUT).until(EC.visibility_of(element))
        text = element.text.strip()
        print(f"📖 Teks dari elemen: {text}")
        return text

    @staticmethod
    def get_text_with_js(element):
        driver = CustomCommand._get_driver_safe()
        try:
            js = driver.execute_script("return arguments[0].textContent;", element)
            return js.strip() if js else ""
        except Exception as e:
            print(f"[WARNING] JS text gagal: {e}. Mencoba fallback .text.")
            try:
                return element.text.strip()
            except Exception:
                return ""

    @staticmethod
    def scroll_into_text(text):
        driver = CustomCommand._get_driver_safe()
        found = False
        max_scroll = 5
        xpath = f"//*[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]"

        for i in range(max_scroll):
            try:
                elements = driver.find_elements(By.XPATH, xpath)
                if elements:
                    el = elements[0]
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", el)
                    print(f"Found and scrolled to: {text}")
                    found = True
                    break
                else:
                    driver.execute_script("window.scrollBy(0, 400);")
                    time.sleep(0.4)
            except Exception as e:
                print(f"⚠️ Scroll attempt {i + 1} failed: {e}")

        if not found:
            raise RuntimeError(f" Text '{text}' tidak ditemukan setelah {max_scroll} kali scroll.")

    @staticmethod
    def scroll_into_view(element):
        driver = CustomCommand._get_driver_safe()
        for attempt in range(CustomCommand.RETRY_COUNT):
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", element)
                time.sleep(CustomCommand.SLEEP_MS)
                return
            except StaleElementReferenceException:
                print(f"⚠️ Stale element, retry {attempt + 1}")
            except Exception as e:
                print(f" Scroll gagal: {e}")
                break

    @staticmethod
    def scroll_to_top():
        driver = CustomCommand._get_driver_safe()
        driver.execute_script("window.scrollTo(0, 0);")
        print(" Scrolled to top")

    @staticmethod
    def scroll_by_pixel(pixels):
        driver = CustomCommand._get_driver_safe()
        driver.execute_script("window.scrollBy(0, arguments[0]);", pixels)
        print(f" Scrolled by {pixels}px")

    @staticmethod
    def scroll_by_coordinate(x, y):
        driver = CustomCommand._get_driver_safe()
        driver.execute_script("window.scrollTo(arguments[0], arguments[1]);", x, y)
        print(f" Scrolled to coordinate ({x}, {y})")

    @staticmethod
    def click_by_coordinate(x, y):
        driver = CustomCommand._get_driver_safe()
        script = """
            var evt = new MouseEvent('click', {clientX: arguments[0], clientY: arguments[1],
                view: window, bubbles: true, cancelable: true});
            document.elementFromPoint(arguments[0], arguments[1]).dispatchEvent(evt);
        """
        driver.execute_script(script, x, y)
        print(f" Clicked at ({x}, {y})")


    @staticmethod
    def wait_until_visible(by):
        driver = CustomCommand._get_driver_safe()
        element = WebDriverWait(driver, CustomCommand.DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located(by)
        )
        print(f"Elemen visible: {by}")
        return element

    @staticmethod
    def sleep(millis):
        try:
            time.sleep(millis / 1000)
        except Exception:
            pass


    @staticmethod
    def get_text_if_present(element):
        try:
            if CustomCommand.is_element_present(element):
                return CustomCommand.get_text_with_js(element)
        except Exception:
            return None
        return None

    @staticmethod
    def refresh_element(supplier_func):
        try:
            return supplier_func()
        except StaleElementReferenceException:
            print("⚠️ Elemen stale, mencoba refresh element...")
            return supplier_func()
