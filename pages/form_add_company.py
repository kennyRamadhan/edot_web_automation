from selenium.webdriver.common.by import By
from base.base_page import BasePage
from helper.custom_command import CustomCommand as cc
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException

class FormAddCompany(BasePage):
    FORM_MESSAGE = (By.XPATH, "//span[@class='mt-10 text-center text-2xl font-bold']")

    FIELD_COMPANY_NAME = (By.XPATH, "//input[@placeholder='Input Company Name']")
    FIELD_COMPANY_EMAIL = (By.XPATH, "//input[@placeholder='Input Email']")
    FIELD_COMPANY_PHONE = (By.XPATH, "//input[@placeholder='Input Phone']")
    SELECT_INDUSTRY = (By.XPATH,"//span[normalize-space()='Choose Industry Type']")
    SELECT_COMPANY_TYPE = (By.XPATH,"//span[normalize-space()='Choose Company Type']")
    LANGUAGE_DROPDOWN = (By.XPATH, "//span[normalize-space()='Choose Language']")
    COUNTRY_DROPDOWN = (By.XPATH, "//span[normalize-space()='Choose Country']")
    FIELD_ADDRESS = (By.XPATH, "//input[@placeholder='Input Address']")
    PROVINCE_DROPDOWN = (By.XPATH, "//span[normalize-space()='Choose Province']")
    SEARCH_ADDRESS=(By.XPATH, "//input[@placeholder='Search']")
    CITY_DROPDOWN = (By.XPATH, "//span[normalize-space()='Choose City']")
    DISTRICT_DROPDOWN = (By.XPATH, "//span[normalize-space()='Choose District']")
    SUB_DISTRICT_DROPDOWN = (By.XPATH, "//span[normalize-space()='Choose Sub District']")
    BUTTON_NEXT = (By.XPATH, "//button[normalize-space()='Next']")
    BUTTON_SAME_AS_COMPANY_ADDRESS = (By.XPATH, "//button[contains(text(),'Fill in with the same data from the Company record')]")
    BUTTON_RESET= (By.XPATH, "//button[normalize-space()='Reset']")
    FIELD_BRANCH= (By.XPATH, "//input[@placeholder='Input Branch Name']")
    CHECKBOX_POLICY= (By.XPATH, "//button[@id='select-all']")
    BUTTON_REGISTER = (By.XPATH, "//button[normalize-space()='Register']")

    OPTION_XPATH_TEMPLATE = "//span[normalize-space()='{}']"
    OPTION_TEMPLATE_ADDRESS = "//div[@cmdk-item and normalize-space(text())='{}']"
    OPTION_XPATH_COUNTRY = "//div[@role='option']//span[normalize-space(text())='{}']"


    def __init__(self, driver):
        super().__init__(driver) 

    def is_form_add_company_displayed(self):
        return self.wait_until_visible(self.FORM_MESSAGE)

      
    def input_company_name(self,company):
        self.type_text(self.FIELD_COMPANY_NAME,company)


    def input_company_email(self,email):
        self.type_text(self.FIELD_COMPANY_EMAIL,email)


    def input_phone_number(self,phone_number):
        self.type_text(self.FIELD_COMPANY_PHONE,phone_number)

    def select_industry(self,industry_name):
        self.click(self.SELECT_INDUSTRY)
        option_locator = (By.XPATH, self.OPTION_XPATH_TEMPLATE.format(industry_name))
        option = self.find_element(*option_locator)
        self.safe_click(option)
    
    
    def select_company_type(self,company_type):
        self.click(self.SELECT_COMPANY_TYPE)
        option_locator = (By.XPATH, self.OPTION_XPATH_TEMPLATE.format(company_type))
        option = self.find_element(*option_locator)
        self.safe_click(option)
    
    def select_language(self,language):
        self.click(self.LANGUAGE_DROPDOWN)
        option_locator = (By.XPATH, self.OPTION_XPATH_TEMPLATE.format(language))
        option = self.find_element(*option_locator)
        self.safe_click(option)
    
    def input_address(self,address):
        self.type_text(self.FIELD_ADDRESS,address)

    def select_contry(self,country):
        self.click(self.COUNTRY_DROPDOWN)
        option_locator = (By.XPATH, self.OPTION_XPATH_COUNTRY.format(country))
        option = self.wait_until_visible(option_locator)    
        self.safe_click(option)

        next_button = self.find_element(*self.BUTTON_NEXT)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)


    def select_dropdown_with_search(self, dropdown_locator, search_text, timeout=10, retries=3):
        """
        Memilih option dari dropdown dengan search, tahan StaleElementReferenceException dan animasi.
        
        Args:
            dropdown_locator: locator dropdown (By, value)
            search_text: text yang ingin dicari dan dipilih
            timeout: waktu tunggu maksimal tiap step
            retries: jumlah retry jika StaleElementReferenceException
        """
        for attempt in range(retries):
            try:
                # Klik dropdown
                dropdown = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(dropdown_locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
                dropdown.click()
                time.sleep(0.2)  # tunggu animasi dropdown
                
                # Tunggu search input muncul
                search_input = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(self.SEARCH_ADDRESS)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_input)
                time.sleep(0.2)
                
                # Bersihkan dan ketik text
                search_input.clear()
                search_input.send_keys(search_text)
                time.sleep(0.3)  # tunggu option muncul
                
                # Tunggu option muncul dan klik
                option_locator = (By.XPATH, self.OPTION_TEMPLATE_ADDRESS.format(search_text))
                option = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(option_locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                option.click()
                return  # sukses, keluar loop
            except (StaleElementReferenceException, ElementClickInterceptedException):
                if attempt < retries - 1:
                    time.sleep(0.3)  # retry
                else:
                    raise


    def select_province(self, province):
        self.select_dropdown_with_search(self.PROVINCE_DROPDOWN, province)

    def select_city(self, city):
        self.select_dropdown_with_search(self.CITY_DROPDOWN, city)

    def select_district(self, district):
        self.select_dropdown_with_search(self.DISTRICT_DROPDOWN, district)

    def select_sub_district(self, sub_district):
        self.select_dropdown_with_search(self.SUB_DISTRICT_DROPDOWN, sub_district)

    
    def click_button_next(self):
        self.click(self.BUTTON_NEXT)

    def input_branch_name(self,branch_name):
        self.type_text(self.FIELD_BRANCH,branch_name)

    def click_button_same_as_company_address(self):
        self.click(self.BUTTON_SAME_AS_COMPANY_ADDRESS)

    def click_policy_checkbox(self):
        self.click(self.CHECKBOX_POLICY)
    
    def click_register_button(self):
        self.click(self.BUTTON_REGISTER)
    
    
