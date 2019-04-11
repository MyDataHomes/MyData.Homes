import requests
import json


class orderBean:
    orderCount = 0

    def __init__(self, name, train, price, status, departure, arrival,
                 carriage, seat, departure_date, arrival_date):
        self.name = name
        self.train = train
        self.price = price
        self.status = status
        self.departure = departure
        self.arrival = arrival
        self.carriage = carriage
        self.seat = seat
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        orderBean.orderCount += 1


def orderBean_2_json(orderbean):
    return {
        "item": {
            "name": orderbean.name,
            "train": orderbean.train,
            "price": orderbean.price,
            "status": orderbean.status,
        },
        "departure": orderbean.departure,
        "arrival": orderbean.arrival,
        "carriage": orderbean.carriage,
        "seat": orderbean.seat,
        "departure_date": orderbean.departure_date,
        "arrival_date": orderbean.arrival_date,
    }


def get_item_info(cookie, pageIndex):
    Headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'private',
        'content-type': 'text/html; charset=gb2312',
        'cookie': cookie,
        'Host': 'my.ctrip.com',
        'referer': 'https://my.ctrip.com/Home/Order/AllOrder.aspx',
        'upgrade-insecure-requests': '1',
        'user-agent': 'ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }
    url = 'https://my.ctrip.com/Home/Ajax/GetAllOrder.ashx'

    data = {
        'PageSize': 10,
        'PageIndex': pageIndex
    }

    orders = []

    res = requests.post(url, data=data, headers=Headers)
    orders_dict = json.loads(res.content.decode('gbk'))
    for order in orders_dict['OrderEnities']:
        name = order['Passagers'][0]
        train = order['OrderName']
        status = order['OrderStatusName']
        price = order['OrderTotalPrice']
        train_info = order['TrainInfo']['Items'][0]
        departure = train_info['DepartureStation']
        arrival = train_info['ArrivalStation']
        carrige = train_info['CarriageNo']
        seat = train_info['SeatNo']
        departure_date = train_info['DepartureDateStr']
        arrival_date = train_info['ArrivalDateStr']
        orderbean = orderBean(name, train, price, status, departure,
                              arrival, carrige, seat, departure_date, arrival_date)
        orders.append(orderbean)

    return orders


def get_all_orders(cookie):
    buy_actions = []
    pageIndex = 1  # 当前账户只有1页的购票记录
    orders = get_item_info(cookie, pageIndex)
    for index in range(len(orders)):
        buy_action = json.dumps(orders[index], default=orderBean_2_json, ensure_ascii=False)
        buy_actions.append(buy_action)

    return buy_actions


def get_user_action(cookie):
    buy_actions = get_all_orders(cookie)
    user_action_str = {
        'buy_actions': buy_actions
    }
    user_action = json.dumps(user_action_str, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    return user_action


def xc_user_cookie(cookie):
    user_action = get_user_action(str(cookie))
    p = open('xc_user_action.json', 'w+')
    p.seek(0)
    p.write(user_action)
    p.close()


if __name__ == '__main__':
    cookie = ''
    user_action = get_user_action(str(cookie))
    p = open('xc_user_action.json', 'w+')
    p.seek(0)
    p.write(user_action)
    p.close()
