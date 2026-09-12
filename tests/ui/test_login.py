import pytest
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage


pytestmark = pytest.mark.ui


def test_valid_login_shows_welcome_message(driver, base_url):
    page = LoginPage(driver, base_url).open().login("demo@example.com", "Quality123")

    assert page.message() == "Welcome, QA Engineer."


def test_invalid_login_shows_clear_error(driver, base_url):
    page = LoginPage(driver, base_url).open().login("demo@example.com", "wrong-password")

    assert page.message() == "Invalid email or password."


def test_email_is_required(driver, base_url):
    page = LoginPage(driver, base_url).open()
    driver.find_element(*page.PASSWORD).send_keys("Quality123")
    driver.find_element(*page.SUBMIT).click()

    assert driver.find_element(By.CSS_SELECTOR, "#email:invalid").is_displayed()

