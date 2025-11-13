from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from base.base_page import BasePage

class DashboardPage(BasePage):
    PROFILE_ICON = (By.XPATH, "//span[@class='font-semibold']/parent::div")
    LOGOUT_BUTTON = (By.XPATH, "//span[normalize-space()='Logout']/parent::div")
    HOME_HEADER = (By.XPATH, "//a[normalize-space()='Home']")
    COMPANY_HEADER = (By.XPATH, "//a[normalize-space()='Companies']")
    BUTTON_ADD_COMPANY = (By.XPATH, "//button[normalize-space()='+ Add Company']")
    COMPANY_CARD = "//div[contains(@class, 'rounded-lg border bg-card')]"
    COMPANY_NAME_IN_CARD = ".//div[contains(@class,'text-lg') and contains(@class,'font-bold')]"
    MANAGE_BUTTON_IN_CARD = ".//button[normalize-space()='Manage']"

    def click_company_header(self):
        self.click(self.COMPANY_HEADER)

    def click_add_new_company(self):
        self.click(self.BUTTON_ADD_COMPANY)
    
    def click_home_header(self):
        self.click(self.HOME_HEADER)

    def logout_user(self):
        # 1. Tunggu dan klik Ikon Profil (membuka dropdown)
        profile_elem = self.wait_until_clickable(self.PROFILE_ICON)
        self.safe_click(profile_elem)

        # 2. Tunggu dan klik tombol Logout
        # Tunggu tombol Logout muncul di dropdown
        logout_elem = self.wait_until_clickable(self.LOGOUT_BUTTON)
        self.safe_click(logout_elem)
        
        # 3. WAJIB: Tunggu sampai URL berubah ATAU elemen dashboard HILANG
        # Ini adalah langkah kritis untuk memastikan browser telah meninggalkan dashboard.
        
        # Tunggu sampai elemen unik di Dashboard menghilang (Misalnya, tombol "Add New Company")
        # Asumsi: DASHBOARD_HEADER adalah elemen unik di dashboard
        # Ganti DASHBOARD_HEADER dengan locator elemen yang pasti hilang setelah logout.
        try:
            # Tunggu maksimal 15 detik sampai elemen dashboard hilang
            self.wait_until_disappear(self.HOME_HEADER, timeout=15)
            print("Successfully waited for dashboard elements to disappear.")
        except Exception as e:
            # Jika elemen dashboard tidak hilang, anggap logout gagal
            print(f"Warning: Dashboard element still visible after logout attempt: {e}")
            # Jika Timeout, berarti browser tidak kembali ke halaman login

    def get_company_manage_button(self, company_name: str, timeout: int = 30):
        """
        Cari company card berdasarkan nama dan kembalikan tombol Manage.
        Menggunakan WebDriverWait sehingga lebih robust.
        """

        def find_manage(driver):
            try:
                cards = driver.find_elements(By.XPATH, self.COMPANY_CARD)
                for card in cards:
                    try:
                        name_elem = card.find_element(By.XPATH, self.COMPANY_NAME_IN_CARD)
                        if name_elem.text.strip() == company_name:
                            # scroll ke viewport center
                            driver.execute_script(
                                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                card
                            )
                            # ambil tombol Manage
                            manage_btn = card.find_element(By.XPATH, self.MANAGE_BUTTON_IN_CARD)
                            return manage_btn
                    except StaleElementReferenceException:
                        continue
                # kalau belum ketemu, scroll sedikit dan return False untuk retry
                driver.execute_script("window.scrollBy(0, 500);")
                return False
            except StaleElementReferenceException:
                return False

        try:
            return WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(find_manage)
        except TimeoutException:
            return None
