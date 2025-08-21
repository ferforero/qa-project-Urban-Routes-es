import data
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import UrbanRoutesPage



class TestUrbanRoutes:
    driver = None
    page = None

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get(data.urban_routes_url)
        cls.page = UrbanRoutesPage(cls.driver)
        cls.page.wait_loaded()

    def test_01_set_route(self):
        self.page.set_route(data.address_from, data.address_to)
        assert self.page.get_from() == data.address_from
        assert self.page.get_to() == data.address_to

    def test_02_select_comfort_tariff(self):
        self.page.open_tariff_picker()
        self.page.select_comfort_tariff()
        assert self.page.is_comfort_active(), "La tarifa Comfort no quedó activa."

    def test_03_enter_telephone_number(self):
        self.page.open_number_input()
        self.page.telephone_enter(data.phone_number)
        self.page.click_phone_next()
        self.page.enter_sms_code()
        shown = self.page._wait_visible(self.page.PHONE_DISPLAY_TEXT).text
        assert re.sub(r"\D", "", shown).endswith(re.sub(r"\D", "", data.phone_number)), \
            "El número mostrado no coincide con el ingresado."

    def test_04_add_credit_card(self):
        self.page.click_in_method_payment()
        self.page.select_card_in_pay_method()
        self.page.enter_number_and_cvv(data.card_number, data.cvv)
        self.page.submit_add_card()
        self.page.wait_add_card_modal_closed()
        self.page.close_payment_modal()
        shown = self.page._wait_visible(self.page.PAY_METHOD_BUTTON).text.lower()
        assert "tarjeta" in shown and "efectivo" not in shown, \
            f"El método de pago no cambió: ahora muestra “{shown}”."

    def test_05_add_comment(self):
        self.page.add_comment_for_driver(data.message_for_driver)
        assert self.page.get_comment() == data.message_for_driver

    def test_06_add_blanket_and_scarves(self):
        self.page.turn_on_blanket()
        assert self.page.is_blanket_on(), "El switch 'Manta y pañuelos' no quedó encendido."
    def test_07_add_two_icecream(self):
        self.page.add_two_ice_cream()
        assert self.page.get_icecream_text() == "2", "El contador de helados no quedó en 2."

    def test_08_request_taxi_modal(self):
        self.page.order_a_taxi()
        title = self.page.wait_search_modal_title()
        assert "buscar" in title.lower(), f"Esperaba ver 'Buscar…' y obtuve: {title!r}"
    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
