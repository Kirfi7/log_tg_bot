import aiohttp
import requests
import urllib.parse
import datetime
import json


async def get_link(date, nick=None, description=None, category=None, offset=None):
    offset = offset if offset else 0
    description = urllib.parse.quote(description) if description else ""
    nick = nick if nick else ""
    return f"https://logs.blackrussia.online/gslogs/1/api/list-game-logs/?category_id__exact={category}&player_name__exact={nick}&player_id__exact=&player_ip__exact=&transaction_amount__exact=&balance_after__exact=&transaction_desc__ilike=%25{description}%25&time__gte=2023-{date}T00%3A00&time__lte=2023-{date}T23%3A59&order_by=time&offset={offset}&auto=false"


async def get_moment_link(nick, date, time):

    day = date.split('-')[1]
    month = date.split('-')[0]
    if day == "01":
        day = "29"
        month = int(month) - 1
        month = f"0{month}" if month <= 9 else month
    else:
        day = int(day) - 1
        day = f"0{day}" if day <= 9 else day

    return f"https://logs.blackrussia.online/gslogs/1/api/list-game-logs/?category_id__exact=38&player_name__exact={nick}&player_id__exact=&player_ip__exact=&transaction_amount__exact=&balance_after__exact=&transaction_desc__ilike=%25%25&time__gte=2023-{month}-{day}T00%3A00&time__lte=2023-{date}T{time.replace(':', '%3A')}&order_by=time&offset=0&auto=false"


async def get_logs_link(nick, start_date, offset):
    day, month = start_date.split(".")
    now_date = datetime.date.today()
    end_date = datetime.date(2023, int(month), int(day)) + datetime.timedelta(days=6)
    if end_date > now_date:
        end_date = now_date
    return f"https://logs.blackrussia.online/gslogs/1/api/list-game-logs/?category_id__exact=&player_name__exact={nick}&player_id__exact=&player_ip__exact=&transaction_amount__exact=&balance_after__exact=&transaction_desc__ilike=%25%25&time__gte=2023-{month}-{day}T00%3A00&time__lte={end_date}T23%3A59&order_by=time&offset={offset}&auto=false"


async def get_response(url):
    with open("settings.json", mode="r+") as file:
        data = json.load(file)

    async with aiohttp.ClientSession(cookies=data['session']) as session:
        async with session.get(url) as response:
            return await response.json()


async def get_count_per_day(date, category, description):
    offset, count = 0, 0

    while True:
        link = await get_link(date=date, category=category, description=description, offset=offset)
        response = await get_response(link)
        json_len = len(response)
        count += json_len

        if json_len == 200:
            offset += 200
        else:
            break
    return count
