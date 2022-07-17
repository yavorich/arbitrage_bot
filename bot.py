import os.path

from telethon import TelegramClient
from p2p_parser import parse
from paysend_parser import parse_ps
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
import asyncio
from datetime import datetime
from pytz import timezone
from csv import writer


async def handle_error(msg):
    print('\n\n\n', msg, '\n\n\n')
    await asyncio.sleep(5)


def get_uzs():
    with open('uzs.txt', 'r') as f:
        rub_uzs = float(f.read())
    return rub_uzs


def count_spread(rub_uzs, uzs_usdt, usdt_rub):
    spread = (1 - uzs_usdt / rub_uzs / usdt_rub) * 100
    return round(spread, 2)


def get_datetime():
    dt = datetime.now(tz=timezone('Europe/Moscow'))
    return dt.date(), dt.weekday(), dt.strftime("%H:%M")


def save_stats(spread, uzs_usdt, usdt_rub):
    col_names = ['date', 'weekday', 'time', 'rub_uzs',
                 'uzs_usdt', 'usdt_rub', 'spread']
    stats_path = 'logs/stats.csv'
    d, wd, t = get_datetime()
    rub_uzs = get_uzs()
    if not os.path.exists(stats_path):
        with open('logs/stats.csv', 'a+') as f:
            writer_object = writer(f)
            writer_object.writerow(col_names)
    with open('logs/stats.csv', 'a') as f:
        writer_object = writer(f)
        writer_object.writerow([d, wd, t, rub_uzs,
                                uzs_usdt, usdt_rub, spread])


async def message():
    while True:
        try:
            uzs_usdt = parse(driver, urls['uzs_usdt'], xpath, sleep=10)
            print('\n\n\n uzs_usdt parsed! \n\n\n')
            usdt_rub = parse(driver, urls['usdt_rub'], xpath, sleep=10)
            print('\n\n\n usdt_rub parsed! \n\n\n')
            rub_uzs = parse_ps(driver)
            print('\n\n\n rub_uzs parsed! \n\n\n')
        except WebDriverException:
            await handle_error('page down')
            continue
        except AttributeError:
            await handle_error('got None value')
            continue
        spread = count_spread(rub_uzs, uzs_usdt, usdt_rub)
        msg = f'spread: {spread}%\n' \
              f'rub_uzs: {rub_uzs}\n' \
              f'uzs_usdt: {uzs_usdt}\n' \
              f'usdt_rub: {usdt_rub}'

        if spread > 1.5:
            msg = '!' + msg
        save_stats(spread, uzs_usdt, usdt_rub)
        await bot.send_message(user_id, msg)
        await asyncio.sleep(50)

if __name__ == '__main__':
    api_id = 12940901
    api_hash = 'a29b8a27154569660285d1f94ffc6ae9'
    bot_token = '5426997463:AAFXiIKKH4x4OfBAJMlIuE_fI8tSO37-7aY'
    bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

    user_id = 'evilp1ranya'
    urls = {
        'uzs_usdt': 'https://p2p.binance.com/ru/trade/all-payments/USDT?fiat=UZS',
        'usdt_rub': 'https://p2p.binance.com/ru/trade/sell/USDT?fiat=RUB&payment=RosBank'
    }
    xpath = '//div[@data-tutorial-id="trade_price_limit"]//text()'

    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(executable_path='C:/ChromeDriver/chromedriver.exe', options=op)

    bot.loop.create_task(message())
    bot.loop.run_forever()
