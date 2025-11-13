# pages/company_detail.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from base.base_page import BasePage

class CompanyDetailPage(BasePage):
    FIELD_MAP = {
        "company_name": (By.XPATH, "//input[@placeholder='Input Company Name']"),
        "email": (By.XPATH, "//input[@placeholder='Input Email']"),
        "phone": (By.XPATH, "//input[@placeholder='Input Mobile Number']"),
        "address": (By.XPATH, "//textarea[@placeholder='Input Company Address']")
    }

    def get_company_field_value(self, field_name: str, timeout=30):
        locator = self.FIELD_MAP.get(field_name)
        if not locator:
            return None

        try:
            elem = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)

            # tunggu sampai value terisi (max timeout)
            # tunggu sampai value terisi (max timeout)
            def value_present(d):
                v = elem.get_attribute("value") or elem.text
                # Tambahkan pemeriksaan: pastikan setelah strip() string tidak kosong
                stripped_v = v.strip() if v else ""
                return stripped_v if stripped_v != "" else False # Jika tidak kosong, kembalikan nilainya
            
            value = WebDriverWait(self.driver, timeout).until(
                value_present, 
                message=f"Timeout waiting for non-empty value in field: {field_name}" # Tambahkan pesan error yang jelas
            )
            import re
            if field_name == "phone":
                value = re.sub(r'\D', '', value)
            elif field_name == "address":
                value = ' '.join(value.split())

            return value.strip()
        except (TimeoutException, StaleElementReferenceException) as e:
            print(f"DEBUG WARNING: Timeout or Stale element while getting value for {field_name}. Error: {e}")
            return ""