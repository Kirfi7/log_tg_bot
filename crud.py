import json
import datetime
import urllib.parse

from table import get_admin_list, get_helpers_dict
from request import get_link, get_response, get_moment_link, get_count_per_day, get_logs_link
from cfg import req_types


async def true_date(text):
    if len(text) == 5 and text[2] == ".":
        try:
            int(text[:2] + text[3:])
        except ValueError:
            return 0
    else:
        return 0
    return 1


async def true_time(text):
    if " " in text:
        first, second = text.split()
        if not await true_date(first):
            return 0
        if ":" in second:
            try:
                int(second.split(":")[0])
                int(second.split(":")[1])
            except ValueError:
                return 0
    return 1


async def true_params(text):
    if " " in text:
        try:
            int(text.split()[0])
            int(text.split()[1])
        except ValueError:
            return 0
    else:
        return 0
    return 1


async def get_top(date, description, category, params=None):
    dictionary, offset = {}, 0
    date = date.split(".")[::-1]

    while True:

        link = await get_link(date=f"{date[0]}-{date[1]}", description=description, category=category, offset=offset)
        response = await get_response(link)

        for tup in response:
            if tup["player_name"] in dictionary:
                dictionary[tup["player_name"]] += 1
            else:
                dictionary[tup["player_name"]] = 1

        if len(response) == 200:
            offset += 200
            continue
        break

    message, k = "", 0
    top = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))

    if params:
        first, diff, last_key = list(map(int, params)) + [999]

        for key in list(top.keys())[:5]:
            if key == last_key:
                k -= 1
            message += f"{k+1}. {key} +{first - diff * k} ответов\n"
            last_key = key
            k += 1

    else:
        for key in top:
            k += 1
            message += f"{k}. {key}: {top[key]}\n"
        message += f"\nВсего за день: {sum(top.values())}"

    return message


async def get_online(moment_date, moment_time):
    nick_list = []
    date = moment_date.split(".")[::-1]
    for nick_name in await get_admin_list():

        link = await get_moment_link(nick=nick_name, date=f"{date[0]}-{date[1]}", time=moment_time)
        response = await get_response(link)
        try:
            if "подключился" in response[0]['transaction_desc']:
                nick_list.append(nick_name)
        except:
            continue

    return nick_list


async def get_stats_text(date):
    new_date = date.split(".")[::-1]
    new_date = f"{new_date[0]}-{new_date[1]}"
    return F"Статистика по серверу за {date}:\n\n" \
           F"Обработано жалоб: {await get_count_per_day(new_date, **req_types['Репорты'])}\n" \
           F"Обработано вопросов: {await get_count_per_day(new_date, **req_types['Вопросы'])}\n" \
           F"Выдано jail'ов: {await get_count_per_day(new_date, **req_types['Джаилы'])}\n" \
           F"Выдано mute'ов: {await get_count_per_day(new_date, **req_types['Муты'])}\n" \
           F"Проведено мероприятий: {await get_count_per_day(new_date, **req_types['Мероприятия'])}"


async def get_helpers_stats():
    ask = {}
    for nick, date in await get_helpers_dict():
        day, month, year = date.split('.')
        for offset in range(0, 2_000_000, 200):
            link = f"https://logs.blackrussia.online/gslogs/1/api/list-game-logs/?category_id__exact=40&player_name__exact={nick}&player_id__exact=&player_ip__exact=&transaction_amount__exact=&balance_after__exact=&transaction_desc__ilike=%25{urllib.parse.quote(']. Ответил')}%25&time__gte=2023-{month}-{day}T00%3A00&time__lte={datetime.date.today()}T23%3A59&order_by=time&offset={offset}&auto=false"
            response = await get_response(link)
            if response:
                ask[nick] = len(response) if nick not in ask else ask[nick] + len(response)
            if len(response) < 200:
                break
    st = ""
    ask = dict(sorted(ask.items(), key=lambda item: item[1], reverse=True))
    for key in ask:
        st += f"{key}: {ask[key]}\n"
    return st


async def get_chief_logs(start_date):
    logs, chief = [], ["Kirfi_Marciano", "Prokhor_Adzinets", "Mikhail_Pearson", "Serega_Forestry"]

    for nick in chief:
        offset = 0
        while True:
            link = await get_logs_link(nick=nick, start_date=start_date, offset=offset)
            response = await get_response(link)
            json_len = len(response)

            if json_len == 200:
                offset += 200
            else:
                logs.append(offset + json_len)
                break

    message = "Количество логов за неделю:\n\n"
    for nick, value in zip(chief, logs):
        message += f"{nick}: {value} логов\n"
    return message


async def set_session_id(session):
    with open("settings.json", mode="r+") as file:
        data = json.load(file)
        data['session']['sessionid'] = session
        file.seek(0)
        json.dump(data, file, indent=2)
