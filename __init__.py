import random
import time
from typing import Union

import numpy
from nonebot import on_startswith
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent

daily = on_startswith(('daily', 'dl'), priority=5, block=True)
lottery = on_startswith(('lottery', 'lt'), priority=5, block=True)


def get_status(num: int):
    if num > 90:
        status = '看起来不错！'
    elif 70 <= num < 90:
        status = '看起来还行？'
    elif 40 <= num < 70:
        status = '看起来一般~'
    elif 10 <= num < 40:
        status = '物极必反！'
    else:
        status = '一定是系统出错了！！'
    return status


@daily.handle()
async def daily_f(event: Union[GroupMessageEvent, PrivateMessageEvent]):
    ids = event.user_id
    today = time.localtime(time.time())
    rand_time = today.tm_year + today.tm_mon * today.tm_mday
    num = (ids / 1000 * rand_time) % 100 + 1
    status = get_status(num)
    date = f"{today.tm_mon}月{today.tm_mday}日，今日运气为{int(num)}，{status}"
    await daily.finish(message=date)


@lottery.handle()
async def lottery_f(event: Union[GroupMessageEvent, PrivateMessageEvent]):
    msg: str = event.message[0].data['text']
    msg_list = msg.split(' ')
    if len(msg_list) == 1:
        num = random.randrange(0, 100)
        status = get_status(num)
        text = f"这一抽抽到了{num}，{status}"
    else:
        times: int = int(msg_list[-1])
        num = [random.randrange(0, 100) for _ in range(times)]
        status = get_status(numpy.average(num))
        text = f"{times}连抽哦，分别抽到了{'、'.join(map(str, num))}，{status}"
    await lottery.finish(message=text)
