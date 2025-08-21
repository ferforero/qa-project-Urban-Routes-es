from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from helpers import retrieve_phone_code

class UrbanRoutesPage:
    # ---- Localizadores
    # Test 1
    FROM_FIELD = (By.ID, "from")
    TO_FIELD   = (By.ID, "to")

    # Test 2
    REQUEST_TAXI_BUTTON = (By.XPATH, "//button[normalize-space()='Pedir un taxi']")
    TARIFF_PANEL = (By.CSS_SELECTOR, "div.tariff-picker.shown")
    MODE_COMFORT_CARD = (
        By.XPATH,
        "//div[contains(@class,'tariff-picker') and contains(@class,'shown')]"
        "//div[contains(@class,'tcard')][.//div[normalize-space()='Comfort']]"
    )
    MODE_COMFORT_CARD_ACTIVE = (
        By.XPATH,
        "//div[contains(@class,'tariff-picker') and contains(@class,'shown')]"
        "//div[contains(@class,'tcard') and contains(@class,'active')]"
        "[.//div[normalize-space()='Comfort']]"
    )

    # Test 3
    TELEPHONE_NUMBER_FIELD = (By.CSS_SELECTOR, ".np-button")
    TELEPHONE_NUMBER_WINDOW = (By.CSS_SELECTOR, ".number-picker.open .section.active")
    TELEPHONE_NUMBER_INPUT = (By.ID, "phone")
    TELEPHONE_NEXT_BUTTON = (By.XPATH, "//form[.//input[@id='phone']]//button[@type='submit']")
    SMS_FIELD = (By.CSS_SELECTOR, ".number-picker.open .section.active input#code")
    SMS_CONFIRM_BUTTON = (By.XPATH, "//form[.//input[@id='code']]//button[@type='submit']")
    PHONE_DISPLAY_TEXT = (By.CSS_SELECTOR, ".np-button .np-text")

    # Test 4
    PAY_METHOD_BUTTON = (By.CSS_SELECTOR, ".pp-button.filled")
    PAYMENT_FIRST_MODAL = (By.CSS_SELECTOR, ".payment-picker.open .section.active")
    ADD_CARD_ROW = (
        By.XPATH,
        "//div[contains(@class,'payment-picker') and contains(@class,'open')]"
        "//div[contains(@class,'pp-title') and normalize-space()='Agregar tarjeta']"
        "/ancestor::div[contains(@class,'pp-row')]"
    )
    PAYMENT_SECOND_MODAL = (By.CSS_SELECTOR, ".payment-picker.open .modal.unusual")
    CARD_NUMBER_FIELD = (By.ID, "number")
    CARD_CVV_FIELD = (By.CSS_SELECTOR, ".payment-picker.open .modal.unusual input#code.card-input")
    ADD_CARD = (By.CSS_SELECTOR, ".payment-picker.open .modal.unusual form button.button.full[type='submit']")
    CLOSE_PAYMENT_MODAL_BUTTON = (By.CSS_SELECTOR, ".payment-picker.open .section.active > button.close-button.section-close")

    # Test 5
    ADD_COMMENT = (By.ID, "comment")

    # Test 6
    BLANKET_SLIDER = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span")
    BLANKET_INPUT  = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/input")
    #Test 7
    ICECREAM_PLUS = (By.XPATH,
                     "//div[contains(@class,'r-type-group')][.//div[contains(@class,'r-group-title') and normalize-space()='Cubeta de helado']]"
                     "//div[contains(@class,'r-type-counter')][.//div[contains(@class,'r-counter-label') and normalize-space()='Helado']]"
                     "//div[contains(@class,'counter-plus')]")
    ICECREAM_VALUE = (By.XPATH,
                      "//div[contains(@class,'r-type-group')][.//div[contains(@class,'r-group-title') and normalize-space()='Cubeta de helado']]"
                      "//div[contains(@class,'r-type-counter')][.//div[contains(@class,'r-counter-label') and normalize-space()='Helado']]"
                      "//div[contains(@class,'counter-value')]")
    # Test 8
    ORDER_A_TAXI_BUTTON= (By.CLASS_NAME, "smart-button-main")
    BUTTON_TAXI_TITLE = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---- Helpers de espera
    def _wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    # ---- Métodos de página
    # Test 1
    def wait_loaded(self):
        self._wait_visible(self.FROM_FIELD)

    def set_route(self, from_address: str, to_address: str):
        from_el = self._wait_visible(self.FROM_FIELD)
        from_el.clear()
        from_el.send_keys(from_address)
        to_el = self._wait_visible(self.TO_FIELD)
        to_el.clear()
        to_el.send_keys(to_address)

    def get_from(self) -> str:
        return self.driver.find_element(*self.FROM_FIELD).get_property("value")

    def get_to(self) -> str:
        return self.driver.find_element(*self.TO_FIELD).get_property("value")

    # Test 2
    def open_tariff_picker(self):
        self._wait_clickable(self.REQUEST_TAXI_BUTTON).click()
        self._wait_visible(self.TARIFF_PANEL)

    def select_comfort_tariff(self):
        if not self.driver.find_elements(*self.TARIFF_PANEL):
            self.open_tariff_picker()
        self._wait_clickable(self.MODE_COMFORT_CARD).click()
        self._wait_visible(self.MODE_COMFORT_CARD_ACTIVE)

    def is_comfort_active(self) -> bool:
        return len(self.driver.find_elements(*self.MODE_COMFORT_CARD_ACTIVE)) > 0

    # Test 3
    def open_number_input(self):
        self._wait_clickable(self.TELEPHONE_NUMBER_FIELD).click()
        self._wait_visible(self.TELEPHONE_NUMBER_WINDOW)

    def telephone_enter(self, number: str):
        field = self._wait_visible(self.TELEPHONE_NUMBER_INPUT)
        field.clear()
        field.send_keys(number)
        field.send_keys(Keys.TAB)

    def click_phone_next(self):
        self._wait_clickable(self.TELEPHONE_NEXT_BUTTON).click()

    def enter_sms_code(self):
        sms_field = self._wait_visible(self.SMS_FIELD)
        sms_field.clear()
        code = retrieve_phone_code(self.driver)
        sms_field.send_keys(code)
        sms_field.send_keys(Keys.TAB)
        self._wait_clickable(self.SMS_CONFIRM_BUTTON).click()

    def wait_sms_field_gone(self) -> bool:
        try:
            self.wait.until(EC.invisibility_of_element_located(self.SMS_FIELD))
            return True
        except TimeoutException:
            return False

    # Test 4
    def click_in_method_payment(self):
        self._wait_clickable(self.PAY_METHOD_BUTTON).click()
        self._wait_visible(self.PAYMENT_FIRST_MODAL)

    def select_card_in_pay_method(self):
        self._wait_clickable(self.ADD_CARD_ROW).click()
        self._wait_visible(self.PAYMENT_SECOND_MODAL)

    def enter_number_and_cvv(self, number: str, cvv: str):
        num_box = self._wait_visible(self.CARD_NUMBER_FIELD)
        num_box.clear()
        num_box.send_keys(number)
        cvv_box = self._wait_visible(self.CARD_CVV_FIELD)
        cvv_box.clear()
        cvv_box.send_keys(cvv)
        cvv_box.send_keys(Keys.TAB)  # habilita el botón

    def submit_add_card(self):
        self._wait_clickable(self.ADD_CARD).click()

    def wait_add_card_modal_closed(self):
        self.wait.until(EC.invisibility_of_element_located(self.PAYMENT_SECOND_MODAL))

    def close_payment_modal(self):
        self._wait_clickable(self.CLOSE_PAYMENT_MODAL_BUTTON).click()
        self.wait.until(EC.invisibility_of_element_located(self.PAYMENT_FIRST_MODAL))

    # Test 5
    def add_comment_for_driver(self, comment):
        box = self._wait_visible(self.ADD_COMMENT)
        box.clear()
        box.send_keys(comment)

    def get_comment(self) -> str:
        return self.driver.find_element(*self.ADD_COMMENT).get_property("value")

    # Test 6
    def turn_on_blanket(self):
        self._wait_clickable(self.BLANKET_SLIDER).click()

    def is_blanket_on(self) -> bool:
        check = self.wait.until(EC.presence_of_element_located(self.BLANKET_INPUT))
        return check.is_selected()
    # Test 7
    def add_two_ice_cream(self):
        btn_add = self._wait_clickable(self.ICECREAM_PLUS)
        btn_add.click()
        btn_add = self._wait_clickable(self.ICECREAM_PLUS)
        btn_add.click()

    def get_icecream_text(self) -> str:
        return self._wait_visible(self.ICECREAM_VALUE).text.strip()
    # Test 8
    def order_a_taxi(self):
        self._wait_clickable(self.ORDER_A_TAXI_BUTTON).click()
    def wait_search_modal_title(self) -> str:
        el = self._wait_visible(self.BUTTON_TAXI_TITLE)
        return (el.text or "").strip()
