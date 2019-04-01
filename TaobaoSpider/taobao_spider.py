import requests
import re
import json


# -*- coding: UTF-8 -*-

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


def get_onepage_orders(pageNum, cookie):
    Headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9',
               'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'cookie': cookie,
               'origin': 'https://buyertrade.taobao.com',
               'referer': 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm',
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
               'x-requested-with': 'XMLHttpRequest'}

    url = 'https://buyertrade.taobao.com/trade/itemlist/asyncBought.htm?action=itemlist/BoughtQueryAction&event_submit_do_query=1&_input_charset=utf8'

    data = {
        'pageNum': pageNum,
        'pageSize': 15,
    }

    orders = []

    res = requests.post(url, data=data, headers=Headers)
    orders_dictx = json.loads(res.content.decode('gbk'))
    for order in orders_dictx['mainOrders']:
        date = order["orderInfo"]["createDay"]
        for index in range(len(order["subOrders"])):
            title = order["subOrders"][index]["itemInfo"]["title"]
            if (title == "保险服务"): continue
            price = order["subOrders"][index]["priceInfo"]["realTotal"]
            quantity = order["subOrders"][index]["quantity"]
            orderbean = orderBean(title, price, quantity, date)
            orders.append(orderbean)

    return orders


def get_all_orders(cookie):
    buy_actions = []
    for pageNum in range(1, 30):
        print('正在读取第%d页数据' % pageNum)
        orders = get_onepage_orders(pageNum, cookie)
        if len(orders) == 0: break
        for index in range(len(orders)):
            buy_action = json.dumps(orders[index], default=orderBean_2_json, ensure_ascii=False)
            buy_actions.append(buy_action)
    return buy_actions


def get_user_action(cookie):
    buy_actions = get_all_orders(cookie)
    user_action_str = {
        "buy_action": buy_actions,
    }
    user_action = json.dumps(user_action_str, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    return user_action


def taobao_user_cookie(cookie):
    user_action = get_user_action(cookie)
    p = open('user_action.json', 'w+')
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
