import requests
import urllib.parse
from cfg import session


async def get_link(date, nick=None, description=None, category=None, offset=None):
    offset = offset if offset else 0
    description = urllib.parse.quote(description)
    nick = nick if nick else ''
    return f"https://logs.blackrussia.online/gslogs/1/api/list-game-logs/?category_id__exact={category}&player_name__exact={nick}&player_id__exact=&player_ip__exact=&transaction_amount__exact=&balance_after__exact=&transaction_desc__ilike=%25{description}%25&time__gte=2023-{date}T00%3A00&time__lte=2023-{date}T23%3A59&order_by=time&offset={offset}&auto=false"


async def get_response(url):
    return requests.get(url=url, cookies=session).json()
