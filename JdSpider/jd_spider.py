import requests
import re
import json


class orderBean:
    orderCount = 0

    def __init__(self, title, price, quantity, date):
        self.title = title
        self.price = price
        self.quantity = quantity
        self.date = date
        orderBean.orderCount += 1


def orderBean_2_json(orderbean):
    return {
        "item": {
            "title": orderbean.title,
            "price": orderbean.price
        },
        "date": orderbean.date,
        "quantity": orderbean.quantity
    }


def get_itemInfo(cookie, itemurl):
    Headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'referer': 'https://order.jd.com/center/list.action',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }
    url = 'https://details.jd.com/normal/item.action?' + itemurl

    res = requests.get(url, headers=Headers)
    content = res.text
    tmp = re.findall('付款时间.*?">.*?\d(.*?)\s', content, re.S)
    if not tmp:
        return 1

    date = "2" + tmp[0]
    namelist = re.findall('class="a-link"  target="_blank" title="(.*?)"', content, re.S)
    pricelist = re.findall('</td>.*?<span class="f-price">(.*?)</span>', content, re.S)
    quantitylist = re.findall('<td>(\d)</td>\s*<td id', content, re.S)
    newpricelist = []
    for price in pricelist:
        priceindex = price.find("yen")
        if priceindex == -1:
            newpricelist.append("0")
        else:
            newpricelist.append(price[priceindex + 4:priceindex + 8])

    items = []
    for index in range(len(namelist)):
        orderbean = orderBean(namelist[index], newpricelist[index], quantitylist[index], date)
        items.append(orderbean)

    return items


def get_orders_byyear(cookie, year):
    orders_byyear = []

    Headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': cookie,
        'referer': 'https://order.jd.com/center/list.action?search=0&d=' + year + '&s=4096',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }

    url = 'https://order.jd.com/center/list.action?search=0&d=' + year + '&s=4096'
    res = requests.get(url, headers=Headers)

    pattern = '<a href=\"//details.jd.com/normal/item.action\?(.*?)\" clstag=\'click\|keycount\|orderlist\|dingdanxiangqing\' target=\"_blank\">'
    itemurls = re.findall(pattern, res.text)
    for index in range(len(itemurls)):
        items = get_itemInfo(cookie, itemurls[index])
        if items == 1:
            print("cancelled order")
        else:
            orders_byyear.extend(items)

    return orders_byyear


def get_user_action(cookie):
    buy_actions = []
    orders = []

    orders.extend(get_orders_byyear(cookie, '2018'))
    orders.extend(get_orders_byyear(cookie, '2017'))
    orders.extend(get_orders_byyear(cookie, '2016'))
    for index in range(len(orders)):
        buy_action = json.dumps(orders[index], default=orderBean_2_json, ensure_ascii=False)
        buy_actions.append(buy_action)

    user_action_str = {
        "buy_action": buy_actions,
    }
    user_action = json.dumps(user_action_str, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    return user_action


def jd_user_cookie(cookie):
    user_action = get_user_action(cookie)
    p = open('jd_user_action.json', 'w+')
    p.seek(0)
    p.write(user_action)
    p.close()


if __name__ == '__main__':
    # input your own cookie
    cookie = ""
    user_action = get_user_action(cookie)
    p = open('user_action.json', 'w+')
    p.seek(0)
    p.write(user_action)
    p.close()
