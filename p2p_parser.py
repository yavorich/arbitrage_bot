from scrapy import Selector
import time


def parse(driver, url, xpath, sleep):
    driver.get(url)

    time.sleep(sleep)

    sel = Selector(text=driver.page_source)
    item = sel.xpath(xpath).extract_first()
    item = item.replace(',', '')
    return float(item)
