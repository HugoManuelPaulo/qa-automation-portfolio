from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class StorePage:
    SEARCH = (By.ID, "search")
    PRODUCTS = (By.CSS_SELECTOR, ".product h3")
    CART_BADGE = (By.ID, "cart-badge")
    CART_TOTAL = (By.ID, "cart-total")
    CHECKOUT = (By.ID, "checkout-button")
    NAME = (By.ID, "customer-name")
    EMAIL = (By.ID, "customer-email")
    ADDRESS = (By.ID, "customer-address")
    PLACE_ORDER = (By.ID, "place-order")
    CONFIRMATION = (By.ID, "confirmation")
    ORDER_REFERENCE = (By.ID, "order-reference")

    def __init__(self, driver, base_url):
        self.driver, self.base_url = driver, base_url
        self.wait = WebDriverWait(driver, 5)

    def open_authenticated(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.ID, "email").send_keys("demo@example.com")
        self.driver.find_element(By.ID, "password").send_keys("Quality123")
        self.driver.find_element(By.ID, "login-button").click()
        self.wait.until(EC.visibility_of_element_located(self.SEARCH))
        return self

    def search(self, term):
        field = self.driver.find_element(*self.SEARCH)
        field.clear()
        field.send_keys(term)
        return self

    def visible_products(self):
        return [element.text for element in self.driver.find_elements(*self.PRODUCTS)]

    def add_product(self, product_id):
        self.driver.find_element(By.CSS_SELECTOR, f'[data-testid="add-{product_id}"]').click()
        return self

    def cart_count(self):
        return int(self.driver.find_element(*self.CART_BADGE).text.split(": ")[1])

    def cart_total(self):
        return float(self.driver.find_element(*self.CART_TOTAL).text)

    def set_quantity(self, product_id, quantity):
        field = self.driver.find_element(By.CSS_SELECTOR, f'[data-cart-id="{product_id}"] input')
        self.driver.execute_script(
            "arguments[0].value = arguments[1]; "
            "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
            field,
            str(quantity),
        )
        return self

    def checkout(self, name, email, address):
        self.driver.find_element(*self.CHECKOUT).click()
        self.wait.until(EC.visibility_of_element_located(self.NAME)).send_keys(name)
        self.driver.find_element(*self.EMAIL).send_keys(email)
        self.driver.find_element(*self.ADDRESS).send_keys(address)
        self.driver.find_element(*self.PLACE_ORDER).click()
        return self

    def order_reference(self):
        self.wait.until(EC.visibility_of_element_located(self.CONFIRMATION))
        return self.driver.find_element(*self.ORDER_REFERENCE).text
