import re

from enum import Enum

from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class METHOD_TYPE(Enum):
    OCO = 'OCO'
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    STOP_LIMIT = 'STOP_LIMIT'


def buy_order(binance: Chrome, strategy, symbol, open_value, high_value, low_value, close_value):
    binance.find_element(By.XPATH, '//span[@data-testid="BuyTab"]').click()

    if strategy['method']['type'] == METHOD_TYPE.MARKET:
        binance.find_element(
            By.XPATH, '//span[@data-testid="MarketType"]').click()

        total_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-BUY-total"]')
        set_input(total_input, strategy['amount'])

    elif strategy['method']['type'] == METHOD_TYPE.LIMIT:
        binance.find_element(
            By.XPATH, '//span[@data-testid="LimitType"]').click()

        price = get_price(
            strategy['method']['price'], open_value, high_value, low_value, close_value)

        price_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-BUY-price"]')
        set_input(price_input, price)

        total_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-BUY-total"]')
        set_input(total_input, strategy['amount'])

    elif strategy['method']['type'] == METHOD_TYPE.STOP_LIMIT:
        binance.find_element(
            By.XPATH, '//span[@data-testid="stopLimit"]').click()

        stop = get_price(
            strategy['method']['stop'], open_value, high_value, low_value, close_value)
        limit = get_price(
            strategy['method']['limit'], open_value, high_value, low_value, close_value)

        stop_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-BUY-stopPrice"]')
        set_input(stop_input, stop)

        limit_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-BUY-stopLimitPrice"]')
        set_input(limit_input, limit)

        total_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-BUY-total"]')
        set_input(total_input, strategy['amount'])

    elif strategy['method']['type'] == METHOD_TYPE.OCO:
        ActionChains(binance).move_to_element(
            binance.find_elements(By.XPATH, '//div[@data-testid="otherType"]')[1]).perform()
        binance.find_elements(By.XPATH, '//*[text()="OCO"]')[2].click()

        price = get_price(
            strategy['method']['price'], open_value, high_value, low_value, close_value)

        stop = get_price(
            strategy['method']['stop'], open_value, high_value, low_value, close_value)
        limit = get_price(
            strategy['method']['limit'], open_value, high_value, low_value, close_value)

        price_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-BUY-price"]')
        set_input(price_input, price)

        stop_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-BUY-stopPrice"]')
        set_input(stop_input, stop)

        limit_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-BUY-stopLimitPrice"]')
        set_input(limit_input, limit)

        total_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-BUY-total"]')
        set_input(total_input, strategy['amount'])

    # binance.find_element(
    #     By.XPATH, '//button[@id="orderformBuyBtn"]').click()


def sell_order(binance: Chrome, strategy, symbol, open_value, high_value, low_value, close_value):
    binance.find_element(By.XPATH, '//span[@data-testid="SellTab"]').click()

    if strategy['method']['type'] == METHOD_TYPE.MARKET:
        binance.find_elements(
            By.XPATH, '//span[@data-testid="MarketType"]')[1].click()

        exchage_assets = binance.find_element(
            By.XPATH, '//div[@data-bn-type="text"]/h1').text
        available_value = float(binance.find_element(
            By.XPATH, '//div[contains(text(), "Available:")]/../span[contains(text(), "{}")]/../../span'.format(exchage_assets.split('/')[0])).text)

        quantity_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-SELL-quantity"]')
        set_input(quantity_input, strategy['amount'] * available_value)

    elif strategy['method']['type'] == METHOD_TYPE.LIMIT:
        binance.find_elements(
            By.XPATH, '//span[@data-testid="LimitType"]')[1].click()

        price = get_price(
            strategy['method']['price'], open_value, high_value, low_value, close_value)

        price_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-SELL-price"]')
        set_input(price_input, price)

        exchage_assets = binance.find_element(
            By.XPATH, '//div[@data-bn-type="text"]/h1').text
        available_value = float(binance.find_element(
            By.XPATH, '//div[contains(text(), "Available:")]/../span[contains(text(), "{}")]/../../span'.format(exchage_assets.split('/')[0])).text)

        quantity_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-SELL-quantity"]')
        set_input(quantity_input, strategy['amount'] * available_value)

    elif strategy['method']['type'] == METHOD_TYPE.STOP_LIMIT:
        binance.find_elements(
            By.XPATH, '//span[@data-testid="stopLimit"]')[1].click()

        stop = get_price(
            strategy['method']['stop'], open_value, high_value, low_value, close_value)
        limit = get_price(
            strategy['method']['limit'], open_value, high_value, low_value, close_value)

        stop_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-SELL-stopPrice"]')
        set_input(stop_input, stop)

        limit_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-SELL-stopLimitPrice"]')
        set_input(limit_input, limit)

        exchage_assets = binance.find_element(
            By.XPATH, '//div[@data-bn-type="text"]/h1').text
        available_value = float(binance.find_element(
            By.XPATH, '//div[contains(text(), "Available:")]/../span[contains(text(), "{}")]/../../span'.format(exchage_assets.split('/')[0])).text)

        quantity_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-SELL-quantity"]')
        set_input(quantity_input, strategy['amount'] * available_value)

    elif strategy['method']['type'] == METHOD_TYPE.OCO:
        ActionChains(binance).move_to_element(
            binance.find_elements(By.XPATH, '//div[@data-testid="otherType"]')[1]).perform()
        binance.find_elements(By.XPATH, '//*[text()="OCO"]')[2].click()

        price = get_price(
            strategy['method']['price'], open_value, high_value, low_value, close_value)

        stop = get_price(
            strategy['method']['stop'], open_value, high_value, low_value, close_value)
        limit = get_price(
            strategy['method']['limit'], open_value, high_value, low_value, close_value)

        price_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-SELL-price"]')
        set_input(price_input, price)

        stop_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-SELL-stopPrice"]')
        set_input(stop_input, stop)

        limit_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-SELL-stopLimitPrice"]')
        set_input(limit_input, limit)

        exchage_assets = binance.find_element(
            By.XPATH, '//div[@data-bn-type="text"]/h1').text
        available_value = float(binance.find_element(
            By.XPATH, '//div[contains(text(), "Available:")]/../span[contains(text(), "{}")]/../../span'.format(exchage_assets.split('/')[0])).text)

        quantity_input = binance.find_element(
            By.XPATH, '//input[@id="FormRow-SELL-quantity"]')
        set_input(quantity_input, strategy['amount'] * available_value)

    # binance.find_element(
    #     By.XPATH, '//button[@id="orderformSellBtn"]').click()


def set_input(element, value):
    element.click()
    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.DELETE)
    element.send_keys(str(value))


def get_price(obj, open_value, high_value, low_value, close_value):
    obj = obj.replace('O', str(open_value))
    obj = obj.replace('H', str(high_value))
    obj = obj.replace('L', str(low_value))
    obj = obj.replace('C', str(close_value))
    return eval(obj)
