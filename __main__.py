import re
import sys
import time

from tools import METHOD_TYPE
from tools import buy_order, sell_order

from selenium.webdriver.common.by import By

from selenium.webdriver import Chrome, ChromeOptions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


order_regex = re.compile(
    '(\d\s)?(SELL|BUY)[(][A-Z]+[)]\sO\d+([.]\d+)?\sH\d+([.]\d+)?\sL\d+([.]\d+)?\sC\d+([.]\d+)?')

strategies = {
    'BUY': {
        '0': {  # Should be 0,1,2,3,4,5,6,7,8,9 zero is default
            'amount': 100,  # USDT
            'method': {
                'type': METHOD_TYPE.STOP_LIMIT,  # LIMIT, MARKET, STOP-LIMIT, OCO
                'stop': 'H +(0.0001 * H)',
                'limit': 'H',
            }
        },
        '1': {  # Should be 0,1,2,3,4,5,6,7,8,9 zero is default
            'amount': 100,  # USDT
            'method': {
                'type': METHOD_TYPE.STOP_LIMIT,  # LIMIT, MARKET, STOP-LIMIT, OCO
                'stop': 'C +(0.0001 * C)',
                'limit': 'C',
            }
        },
        '2': {  # Should be 0,1,2,3,4,5,6,7,8,9 zero is default
            'amount': 100,  # USDT
            'method': {
                'type': METHOD_TYPE.STOP_LIMIT,  # LIMIT, MARKET, STOP-LIMIT, OCO
                'stop': 'C +(0.0001 * C)',
                'limit': 'C',
            }
        },
        '3': {  # Should be 0,1,2,3,4,5,6,7,8,9 zero is default
            'amount': 100,  # USDT
            'method': {
                'type': METHOD_TYPE.STOP_LIMIT,  # LIMIT, MARKET, STOP-LIMIT, OCO
                'stop': 'H +(0.0001 * H)',
                'limit': 'H',
            }
        },
    },
    'SELL': {
        '0': {  # Should be 0,1,2,3,4,5,6,7,8,9 zero is default
            'amount': 1.0,  # % In Percent Between (0.0 - 1.0)
            'method': {
                'type': METHOD_TYPE.OCO,  # LIMIT, MARKET, STOP-LIMIT, OCO
                'price': '1.1 * (H - L) + H',
                'stop': 'L -(0.0001 * L)',
                'limit': 'L',
            }
        },
        '1': {  # Should be 0,1,2,3,4,5,6,7,8,9 zero is default
            'amount': 1.0,  # % In Percent Between (0.0 - 1.0)
            'method': {
                'type': METHOD_TYPE.OCO,  # LIMIT, MARKET, STOP-LIMIT, OCO
                'price': '1.1 * (C - L) + C',
                'stop': 'L -(0.0001 * L)',
                'limit': 'L',
            }
        },
        '2': {  # Should be 0,1,2,3,4,5,6,7,8,9 zero is default
            'amount': 1.0,  # % In Percent Between (0.0 - 1.0)
            'method': {
                'type': METHOD_TYPE.OCO,  # LIMIT, MARKET, STOP-LIMIT, OCO
                'price': '1.1 * (C - O) + C',
                'stop': 'O -(0.0001 * O)',
                'limit': 'O',
            }
        },
        '3': {  # Should be 0,1,2,3,4,5,6,7,8,9 zero is default
            'amount': 1.0,  # % In Percent Between (0.0 - 1.0)
            'method': {
                'type': METHOD_TYPE.OCO,  # LIMIT, MARKET, STOP-LIMIT, OCO
                'price': '1.1 * (H - O) + H',
                'stop': 'O -(0.0001 * O)',
                'limit': 'O',
            }
        },
    }
}


if __name__ == "__main__":

    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])

    # TradingView

    TradingView = Chrome(options=options)
    TradingView.get('https://www.tradingview.com/')

    WebDriverWait(TradingView, 3*60).until(EC.visibility_of_element_located(
        (By.XPATH, '//img[@class="tv-header__userpic js-userpic-mid"]')))
    TradingView.get('https://www.tradingview.com/chart')

    time.sleep(5)
    TradingView.execute_script(
        'window.__tvb__strategy="0",window.__tvb__symbol=document.evaluate("//div[@id=\'header-toolbar-symbol-search\']",document,null,XPathResult.STRING_TYPE,null).stringValue,window.__tvb__order=`${window.__tvb__strategy} BUY(${window.__tvb__symbol}) O0 H0 L0 C0`,document.addEventListener("click",function(_){window.__tvb__symbol=document.evaluate("//div[@id=\'header-toolbar-symbol-search\']",document,null,XPathResult.STRING_TYPE,null).stringValue,window.__tvb__order=`${window.__tvb__strategy} BUY(${window.__tvb__symbol}) O0 H0 L0 C0`,console.log(`Symbol Changed to ${window.__tvb__symbol}.`)}),document.addEventListener("keyup",function(_){console.log(`Key.${_.key} pressed.`)," "==_.key&&(window.__tvb__symbol=document.evaluate("//div[@id=\'header-toolbar-symbol-search\']",document,null,XPathResult.STRING_TYPE,null).stringValue,window.__tvb__order=`${window.__tvb__strategy} BUY(${window.__tvb__symbol}) O0 H0 L0 C0`,console.log(`Symbol Changed to ${window.__tvb__symbol}.`)),parseInt(_.key)<10&&(window.__tvb__strategy=_.key,console.log(`window.__tvb__strategy --\x3e ${window.__tvb__strategy}`),window.__tvb__order=`${window.__tvb__strategy} BUY(${window.__tvb__symbol}) O0 H0 L0 C0`);const t=document.evaluate("//div[text()=\'O\']/..",document,null,XPathResult.STRING_TYPE,null).stringValue,e=document.evaluate("//div[text()=\'H\']/..",document,null,XPathResult.STRING_TYPE,null).stringValue,o=document.evaluate("//div[text()=\'L\']/..",document,null,XPathResult.STRING_TYPE,null).stringValue,n=document.evaluate("//div[text()=\'C\']/..",document,null,XPathResult.STRING_TYPE,null).stringValue;switch(_.key){case"Enter":window.__tvb__order=`${window.__tvb__strategy} BUY(${window.__tvb__symbol}) ${t} ${e} ${o} ${n}`,console.log(`window.__tvb__order --\x3e ${window.__tvb__order}`);break;case"Backspace":window.__tvb__order=`${window.__tvb__strategy} SELL(${window.__tvb__symbol}) ${t} ${e} ${o} ${n}`,console.log(`window.__tvb__order --\x3e ${window.__tvb__order}`)}});')

    print('[TradingView] TVB-Trader connected.')

    # Binance
    binance_url = 'https://www.binance.com/en/trade/{}?type=' + \
        sys.argv[1].lower()

    Binance = Chrome(options=options)
    Binance.get('https://accounts.binance.com/')

    WebDriverWait(Binance, 3*60).until(EC.visibility_of_element_located(
        (By.XPATH, '//div[contains(@class, "header_user_info")]')))

    Binance.get(binance_url.format(
        str(TradingView.execute_script('return window.__tvb__symbol;'))))

    print('[Binance] TVB-Trader connected.')

    tvb_strategy = str(TradingView.execute_script(
        'return window.__tvb__strategy;'))
    tvb_symbol = str(TradingView.execute_script(
        'return window.__tvb__symbol;'))
    tvb_order = str(TradingView.execute_script(
        'return window.__tvb__order;'))

    while(True):
        try:
            _new_tvb_order = str(TradingView.execute_script(
                'return window.__tvb__order;'))

            if not tvb_order == _new_tvb_order and order_regex.match(_new_tvb_order):
                if not tvb_order[0] == _new_tvb_order[0]:
                    tvb_strategy = _new_tvb_order[0]
                    print(
                        '[TVB-Trader] Strategy changed to {}.'.format(tvb_strategy))

                elif not re.findall('([(][A-Z]+[)])', tvb_order)[0] == re.findall('([(][A-Z]+[)])', _new_tvb_order)[0]:
                    tvb_symbol = re.findall(
                        '([(][A-Z]+[)])', _new_tvb_order)[0][1:-1]
                    Binance.get(binance_url.format(tvb_symbol))
                    print('[TVB-Trader] Assets changed to {}.'.format(tvb_symbol))

                else:
                    tvb_order = _new_tvb_order
                    side = 'BUY' if 'BUY' in tvb_order else 'SELL'

                    open_value = float(re.findall(
                        'O(\d+([.]\d+)?)', tvb_order)[0][0])
                    high_value = float(re.findall(
                        'H(\d+([.]\d+)?)', tvb_order)[0][0])
                    low_value = float(re.findall(
                        'L(\d+([.]\d+)?)', tvb_order)[0][0])
                    close_value = float(re.findall(
                        'C(\d+([.]\d+)?)', tvb_order)[0][0])

                    if side == 'BUY':
                        if tvb_strategy in strategies[side]:
                            buy_order(
                                Binance, strategies[side][tvb_strategy], tvb_symbol, open_value, high_value, low_value, close_value)
                        else:
                            print(
                                '[TVB-Trader] {} buy strategy does`t exist.'.format(tvb_strategy))
                            continue

                    elif side == 'SELL':
                        if tvb_strategy in strategies[side]:
                            sell_order(
                                Binance, strategies[side][tvb_strategy], tvb_symbol, open_value, high_value, low_value, close_value)
                        else:
                            print(
                                '[TVB-Trader] {} sell strategy does`t exist.'.format(tvb_strategy))
                            continue

                    print('[TVB-Trader] New Order Placed {}.'.format(tvb_order))

                tvb_order = _new_tvb_order
        except:
            pass
