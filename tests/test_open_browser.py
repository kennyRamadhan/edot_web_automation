# tests/test_open_browser.py
import re
import allure
import pytest
from base.base_test import BaseTest
from pages.company_detail import CompanyDetailPage
from pages.dashboard import DashboardPage
from pages.form_add_company import FormAddCompany
from pages.login_page import LoginPage
from helper.data_faker import FakerData

@allure.epic("EDOT")
@allure.feature("Registrasi dan Validasi")
class TestOpenBrowser(BaseTest):

    @allure.story("Registrasi Perusahaan Baru")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.e2e
    def test_add_new_company(self):

        # --- Page Objects ---
        login_page = LoginPage(self.driver)
        detail_page = CompanyDetailPage(self.driver)
        dashboard_page = DashboardPage(self.driver)
        form_page = FormAddCompany(self.driver)

        # --- Test Data ---
        company_name = FakerData.get_company()
        email = FakerData.get_email()
        phone = FakerData.get_phone()
        address = FakerData.get_address()

        # --- Step 1: Login ---
        with allure.step("Login ke aplikasi"):
            login_page.login("it.qa@edot.id", "it.QA2025")
            # Screenshot milestone: Login sukses
            login_page.take_screenshot("Login Page")
            assert login_page.is_login_successful(), "Login should be successful"

        # --- Step 2: Navigate to Add New Company ---
        with allure.step("Navigasi ke form tambah perusahaan baru"):
            dashboard_page.click_company_header()
            dashboard_page.click_add_new_company()
            assert form_page.is_form_add_company_displayed(), "Form Add Company tidak tampil"
            # Screenshot milestone: Form tampil
            form_page.take_screenshot("Form Add Company Displayed")

        # --- Step 3: Input Company Details ---
        with allure.step(f"Input semua data perusahaan: {company_name}"):
            form_page.input_company_name(company_name)
            form_page.input_company_email(email)
            form_page.input_phone_number(phone)
            form_page.select_industry("Retail")
            form_page.select_company_type("Marketplace")
            form_page.select_language("Indonesia")
            form_page.input_address(address)
            form_page.select_contry("Indonesia")
            form_page.select_province("JAWA BARAT")
            form_page.select_city("KAB BEKASI")
            form_page.select_district("KARANG BAHAGIA")
            form_page.select_sub_district("SUKARAYA")
            # Screenshot milestone: Semua data input selesai
            form_page.take_screenshot("Company Details Filled")

        # --- Step 4: Input Branch and Policies ---
        with allure.step("Input data cabang dan setujui kebijakan"):
            form_page.click_button_next()
            form_page.click_button_next()
            branch_name = "Branch" + str(FakerData.get_random_number())
            form_page.input_branch_name(branch_name)
            form_page.click_button_same_as_company_address()
            form_page.click_policy_checkbox()
            # Screenshot milestone: Branch & Policy siap
            form_page.take_screenshot("Branch & Policy Checked")
            form_page.click_register_button()

        # --- Step 5: Back to Company Dashboard ---
        with allure.step("Kembali ke dashboard perusahaan"):
            dashboard_page.click_company_header()
            # Screenshot milestone: Dashboard tampil
            dashboard_page.take_screenshot("Dashboard Companies List")

        # --- Step 6: Validate Company Details ---
        with allure.step("Validasi detail perusahaan"):
            manage_btn = dashboard_page.get_company_manage_button(company_name)
            assert manage_btn is not None, f"Company '{company_name}' not found"
            manage_btn.click()
            # Screenshot milestone: Detail company tampil
            detail_page.take_screenshot("Company Detail Page")

            # Normalisasi data untuk perbandingan
            expected_phone_normalized = re.sub(r'\D', '', phone)
            expected_address_content = re.sub(r'[\W_]', '', address).lower()

            # --- Assertions ---
            with allure.step("Validasi nama perusahaan"):
                actual_name = detail_page.get_company_field_value("company_name")
                assert actual_name == company_name, \
                    f"Gagal Validasi Nama Perusahaan. Expected: {company_name}, Actual: {actual_name}"

            with allure.step("Validasi email perusahaan"):
                actual_email = detail_page.get_company_field_value("email")
                assert actual_email == email, \
                    f"Gagal Validasi Email. Expected: {email}, Actual: {actual_email}"

            with allure.step("Validasi nomor telepon (normalized)"):
                actual_phone_normalized = detail_page.get_company_field_value("phone")
                assert actual_phone_normalized == expected_phone_normalized, \
                    f"Gagal Validasi Telepon (Normalized). Expected: {expected_phone_normalized}, Actual: {actual_phone_normalized}"

            with allure.step("Validasi konten alamat perusahaan"):
                actual_address_raw = detail_page.get_company_field_value("address")
                actual_address_content = re.sub(r'[\W_]', '', actual_address_raw).lower()
                assert actual_address_content == expected_address_content, \
                    f"Gagal Validasi Konten Alamat. Expected Content: {expected_address_content}, Actual Content: {actual_address_content}"
