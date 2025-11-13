import pytest
import allure

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook Pytest untuk mengeksekusi setelah setiap test case.
    Jika test gagal, ambil screenshot dan attach ke Allure report.
    """
    outcome = yield
    rep = outcome.get_result()

    # Hanya eksekusi saat test case selesai (call saat fase 'call')
    if rep.when == "call" and rep.failed:
        # Ambil driver dari fixture test case
        driver = item.funcargs.get("driver")
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
