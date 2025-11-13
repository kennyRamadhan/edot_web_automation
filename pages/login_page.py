from selenium.webdriver.common.by import By
from base.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD = (By.XPATH, "//input[@placeholder='Input Email or Username']")
    PASSWORD_FIELD = (By.XPATH, "//input[@placeholder='Password']")
    USE_EMAIL_BUTTON = (By.XPATH, "//button[normalize-space()='Use Email or Username']")
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Log In']")
    WELCOME_MESSAGE = (By.XPATH, "//span[normalize-space()='Welcome Back,']")

    def click_use_email(self):
        self.click(self.USE_EMAIL_BUTTON)

    def enter_username(self, username):
        self.type_text(self.USERNAME_FIELD, username)

    def enter_password(self, password):
        self.type_text(self.PASSWORD_FIELD, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        self.click_use_email()
        self.enter_username(username)
        self.click_login()
        self.enter_password(password)
        self.click_login()
        self.take_screenshot("After Login Click")

    def is_login_successful(self):
        return self.is_visible(self.WELCOME_MESSAGE)
    
    
    def is_login_page_displayed(self, timeout=10):
        # Menunggu sampai field input email/username di halaman login terlihat
        try:
            self.wait_until_visible(self.USERNAME_FIELD, timeout)
            return True
        except:
            return False
