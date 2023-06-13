from request import get_link, get_response, get_moment_link, get_count_per_day
from cfg import req_types


async def true_value(text, separator):
    if len(text) == 5 and text[2] == separator:
        try:
            int(text[:2] + text[3:])
        except ValueError:
            return 0
    else:
        return 0
    return 1


async def true_params(text):
    if "-" in text:
        try:
            int(text.split('-')[0])
            int(text.split('-')[1])
        except ValueError:
            return 0
    else:
        return 0
    return 1


async def get_top(date, description, category, params=None):
    dictionary, offset = {}, 0

    while True:

        link = await get_link(date=date, description=description, category=category, offset=offset)
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
        first, diff = list(map(int, params))

        for key in list(top.keys())[:5]:
            message += f"{k+1}. {key} +{first - diff * k} ответов\n"
            k += 1

    else:
        for key in top:
            k += 1
            message += f"{k}. {key}: {top[key]}\n"
        message += f"\nВсего за день: {sum(top.values())}"

    return message


async def get_online(admin_list, date, time):
    nick_list = []
    for nick_name in admin_list:

        link = await get_moment_link(nick=nick_name, date=date, time=time)
        response = await get_response(link)
        try:
            if "подключился" in response[0]['transaction_desc']:
                nick_list.append(nick_name)
        except:
            continue

    return nick_list


async def get_stats_text(date):
    return F"Статистика по серверу за {date}:\n\n" \
           F"Обработано жалоб: {await get_count_per_day(date, **req_types['/reports'])}\n" \
           F"Обработано вопросов: {await get_count_per_day(date, **req_types['/questions'])}\n" \
           F"Выдано jail'ов: {await get_count_per_day(date, **req_types['/jails'])}\n" \
           F"Выдано mute'ов: {await get_count_per_day(date, **req_types['/mutes'])}\n" \
           F"Проведено мероприятий: {await get_count_per_day(date, **req_types['/events'])}"
