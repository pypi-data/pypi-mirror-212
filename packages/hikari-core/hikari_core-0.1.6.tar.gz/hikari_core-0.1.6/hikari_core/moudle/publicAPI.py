# fmt: off
import asyncio
import gzip
import traceback
from asyncio.exceptions import TimeoutError
from base64 import b64encode
from typing import List, Tuple

import orjson
from bs4 import BeautifulSoup
from httpx import ConnectTimeout
from loguru import logger

from ..data_source import levels, nations, number_url_homes, shiptypes
from ..HttpClient_Pool import (get_client_default, get_client_wg,
                               get_client_yuyuko)
from ..model import Ship_Model
from ..utils import match_keywords

# fmt: on


async def get_nation_list():
    try:
        msg = ""
        url = "https://api.wows.shinoaki.com/public/wows/encyclopedia/nation/list"
        client_yuyuko = await get_client_yuyuko()
        resp = await client_yuyuko.get(url, timeout=None)
        result = orjson.loads(resp.content)
        for nation in result["data"]:
            msg: str = msg + f"{nation['cn']}：{nation['nation']}\n"
        return msg
    except Exception:
        logger.error(traceback.format_exc())


async def get_ship_name(server_type, infolist: List, bot, ev):
    msg = ""
    try:
        param_nation, infolist = await match_keywords(infolist, nations)
        if not param_nation:
            return "请检查国家名是否正确"

        param_shiptype, infolist = await match_keywords(infolist, shiptypes)
        if not param_shiptype:
            return "请检查船只类别是否正确"

        param_level, infolist = await match_keywords(infolist, levels)
        if not param_level:
            return "请检查船只等级是否正确"
        params = {
            "county": param_nation,
            "level": param_level,
            "shipName": "",
            "shipType": param_shiptype,
        }
        url = "https://api.wows.shinoaki.com/public/wows/encyclopedia/ship/search"
        client_yuyuko = await get_client_yuyuko()
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["data"]:
            for ship in result["data"]:
                msg += f"{ship['shipNameCn']}：{ship['shipNameNumbers']}\n"
        else:
            msg = "没有符合的船只"
        return msg
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
    except Exception:
        logger.error(traceback.format_exc())
        return "wuwuwu出了点问题，请联系麻麻解决"


async def get_ship_byName(shipname: str) -> List:
    try:
        url = "https://api.wows.shinoaki.com/public/wows/encyclopedia/ship/search"
        params = {"county": "", "level": "", "shipName": shipname, "shipType": ""}
        client_yuyuko = await get_client_yuyuko()
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        List = []
        if result["code"] == 200 and result["data"]:
            for each in result["data"]:
                List.append(
                    Ship_Model(
                        Ship_Nation=each["country"],
                        Ship_Tier=each["tier"],
                        Ship_Type=each["shipType"],
                        Ship_Name=each["shipNameCn"],
                        ship_Name_Numbers=each["shipNameNumbers"],
                        Ship_Id=each["id"],
                    )
                )
            return List
        else:
            return None
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
    except Exception:
        logger.error(traceback.format_exc())
        return None


async def get_all_shipList():
    try:
        url = "https://api.wows.shinoaki.com/public/wows/encyclopedia/ship/search"
        params = {"county": "", "level": "", "shipName": "", "shipType": ""}
        client_yuyuko = await get_client_yuyuko()
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["data"]:
            return result["data"]
        else:
            return None
    except Exception:
        return None


async def get_AccountIdByName(server: str, name: str) -> str:
    try:
        url = "https://api.wows.shinoaki.com/public/wows/account/search/user"
        params = {"server": server, "userName": name}
        client_yuyuko = await get_client_yuyuko()
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["data"]:
            return int(result["data"]["accountId"])
        else:
            return result["message"]
    except (TimeoutError, ConnectTimeout):
        logger.warning(traceback.format_exc())
        return "请求超时了，请过一会儿重试哦~"
    except Exception:
        logger.error(traceback.format_exc())
        return "好像出了点问题呢，可能是网络问题，如果重试几次还不行的话，请联系麻麻解决"


async def get_ClanIdByName(server: str, tag: str):
    try:
        url = "https://api.wows.shinoaki.com/public/wows/clan/search"
        params = {"server": server, "tag": tag, "type": 1}
        client_yuyuko = await get_client_yuyuko()
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        List = []
        if result["code"] == 200 and result["data"]:
            # for each in result['data']:
            #    List.append([each['clanId'],each['name'],each['serverName'],each['tag']])
            return result["data"]
        else:
            return None
    except Exception:
        logger.error(traceback.format_exc())
        return None


async def check_yuyuko_cache(server, id):
    try:
        yuyuko_cache_url = "https://api.wows.shinoaki.com/api/wows/cache/check"
        params = {"accountId": id, "server": server}
        client_yuyuko = await get_client_yuyuko()
        resp = await client_yuyuko.post(yuyuko_cache_url, json=params, timeout=5)
        result = orjson.loads(resp.content)
        cache_data = {}
        if result["code"] == 201:
            if "DEV" in result["data"]:
                await get_wg_info(cache_data, "DEV", result["data"]["DEV"])
            elif "pvp" in result["data"]:
                tasks = []
                for key in result["data"]:
                    tasks.append(asyncio.ensure_future(get_wg_info(cache_data, key, result["data"][key])))
                await asyncio.gather(*tasks)
            if not cache_data:
                return False
            data_base64 = b64encode(gzip.compress(orjson.dumps(cache_data))).decode()
            params["data"] = data_base64
            resp = await client_yuyuko.post(yuyuko_cache_url, json=params, timeout=5)
            result = orjson.loads(resp.content)
            logger.success(result)
            if result["code"] == 200:
                return True
            else:
                return False
        return False
    except Exception:
        logger.error(traceback.format_exc())
        return False


async def get_wg_info(params, key, url):
    try:
        client_wg = await get_client_wg()
        resp = await client_wg.get(url, timeout=5, follow_redirects=True)
        wg_result = orjson.loads(resp.content)
        if resp.status_code == 200 and wg_result["status"] == "ok":
            params[key] = resp.text
    except Exception:
        logger.error(traceback.format_exc())
        logger.error(f"上报url：{url}")
        return


async def get_MyShipRank_yuyuko(params) -> int:
    try:
        url = "https://api.wows.shinoaki.com/upload/numbers/data/upload/user/ship/rank"
        client_yuyuko = await get_client_yuyuko()
        resp = await client_yuyuko.get(url, params=params, timeout=None)
        result = orjson.loads(resp.content)
        if result["code"] == 200 and result["data"]:
            if result["data"]["ranking"]:
                return result["data"]["ranking"]
            elif not result["data"]["ranking"] and not result["data"]["serverId"] == "cn":
                ranking = await get_MyShipRank_Numbers(result["data"]["httpUrl"], result["data"]["serverId"])
                if ranking:
                    await post_MyShipRank_yuyuko(
                        result["data"]["accountId"],
                        ranking,
                        result["data"]["serverId"],
                        result["data"]["shipId"],
                    )
                return ranking
            else:
                return None
        else:
            return None
    except Exception:
        logger.error(traceback.format_exc())
        return None


async def get_MyShipRank_Numbers(url, server) -> int:
    try:
        data = None
        client_default = await get_client_default()
        client_default = await get_client_default()
        resp = await client_default.get(url, timeout=10)
        if resp.content:
            result = orjson.loads(resp.content)
            page_url = str(result["url"]).replace("\\", "")
            nickname = str(result["nickname"])
            my_rank_url = f"{number_url_homes[server]}{page_url}"
            resp = await client_default.get(my_rank_url, timeout=10)
            soup = BeautifulSoup(resp.content, "html.parser")
            data = soup.select_one(f'tr[data-nickname="{nickname}"]').select_one("td").string
        if data and data.isdigit():
            return data
        else:
            return None
    except Exception:
        logger.error(traceback.format_exc())
        return None


async def post_MyShipRank_yuyuko(accountId, ranking, serverId, shipId):
    try:
        url = "https://api.wows.shinoaki.com/upload/numbers/data/upload/user/ship/rank"
        post_data = {
            "accountId": int(accountId),
            "ranking": int(ranking),
            "serverId": serverId,
            "shipId": int(shipId),
        }
        client_yuyuko = await get_client_yuyuko()
        resp = await client_yuyuko.post(url, json=post_data, timeout=None)
        result = orjson.loads(resp.content)
        return
    except Exception:
        logger.error(traceback.format_exc())
        return
