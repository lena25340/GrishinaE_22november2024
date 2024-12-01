import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import requests



@allure.feature("UI тесты для функционала корзины интернет-магазина.")
@allure.title("Добавление товара в корзину.")
@allure.description("Проверяем, что товар добавлен в корзину.")
def test_add_product_to_cart():
    product_name = "Грибная икра из опят"
    product_url = "https://www.sibdar-spb.ru/"
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    try:
        driver.get(product_url)
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{product_name}')]"))
        )
        add_to_cart_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{product_name}')]/following-sibling::button[contains(text(), 'Добавить в корзину')]"))
        )
        add_to_cart_button.click()
        cart_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/cart')]"))
        )
        cart_button.click()
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{product_name}')]"))
       )
        assert product_name in driver.page_source, f"Товар '{product_name}' не найден в корзине."

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

@allure.feature("UI тесты для функционала корзины интернет-магазина.")
@allure.title("Проверка количества товаров в корзине.")
@allure.description("Проверяем, что количество товаров в корзине соответствует ожидаемому.")
def test_cart_item_count():
    product_name = "Грибная икра из опят"
    product_url = "https://www.sibdar-spb.ru/"
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    try:
        driver.get(product_url)
        add_to_cart_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{product_name}')]/following-sibling::button[contains(text(), 'Добавить в корзину')]"))
        )
        add_to_cart_button.click()
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//span[@class='cart-item-count']"), '1')
        )
        cart_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/cart')]"))
        )
        cart_button.click()
        item_count_element = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='cart-item-count']"))
        )
        item_count = int(item_count_element.text)

        assert item_count == 1, f"Количество товаров в корзине должно быть 1, а не {item_count}."

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

@allure.feature("UI тесты для функционала корзины интернет-магазина.")
@allure.title("Удаление товара из корзины.")
@allure.description("Проверяем, что товар удален из корзины.")
def test_remove_product_from_cart():
    product_name = "Грибная икра из опят"
    product_url = "https://www.sibdar-spb.ru/"
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    try:
        driver.get(product_url)
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{product_name}')]"))
        )
        add_to_cart_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{product_name}')]/following-sibling::button[contains(text(), 'Добавить в корзину')]"))
        )
        add_to_cart_button.click()
        cart_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/cart')]"))
        )
        cart_button.click()
        remove_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{product_name}')]/following-sibling::button[contains(text(), 'Удалить')]"))
        )
        remove_button.click()
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, "//div[@class='cart-empty']"), "Корзина пуста")
        )
        assert product_name not in driver.page_source, f"Товар '{product_name}' все еще находится в корзине."

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()
