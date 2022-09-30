import re
from aiohttp import ClientSession
import re
import json


def parse_cookie_json(path: str):
    cookies = {}
    with open(path, 'r', encoding='utf8') as f:
        c = json.loads(f.read())
        for l in c:
            cookies[l['name']] = l['value']

    return ClientSession(cookies=cookies)


async def get_info(url: str, session: ClientSession):
    page = await (await session.get(url)).text()
    return json.loads(re.findall(r'initialState\d{4} = ([^\n]*);\n', page)[-1])