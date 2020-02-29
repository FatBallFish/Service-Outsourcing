from Hotel import settings
import requests
import json

api_url = "https://restapi.amap.com/v3/config/district"
param_dict = {"key": settings.MAP_KEY, "output": "json"}
param_list = ["key", "keywords", "subdistrict", "page", "offset", "extensions", "filter", "callback", "output"]


def getDistrict(**kwargs) -> dict:
    kwargs.update(param_dict)
    data_list = []
    data_str = ""
    for key in sorted(kwargs):
        if key not in param_list:
            del kwargs[key]
            continue
        data_list.append("{}={}".format(key, kwargs[key]))
    data_str = "&".join(data_list)
    # print(data_str)
    response = requests.get(url=api_url, params=kwargs)
    try:
        data = response.json()
    except Exception as e:
        # status 100 API请求失败
        return {"id": -1, "status": 100, "message": "Get Json Error", "data": {}}
    data["id"] = -1
    if "count" in data.keys():
        del data["count"]
    if "suggestion" in data.keys():
        del data["suggestion"]
    if "districts" in data.keys():
        districts = data["districts"]
        if isinstance(districts, list):
            districts = dealData(districts)
        # data["districts"] = districts
        data["data"] = {"districts": districts}
        del data["districts"]
    if "infocode" in data.keys():
        infocode = int(data["infocode"])
        if infocode == 10000:
            data["status"] = 0
        else:
            data["status"] = infocode
        del data["infocode"]
    if "info" in data.keys():
        data["message"] = data["info"]
        del data["info"]
    return data


def dealData(districts: list) -> list:
    if len(districts) == 0:
        return []
    district: dict = None
    for district in districts:
        if "citycode" in district.keys():
            del district["citycode"]
        if "adcode" in district.keys():
            del district["adcode"]
        if "center" in district.keys():
            del district["center"]
        if "level" in district.keys():
            del district["level"]
        if "districts" in district:
            dealData(district["districts"])
    return districts


if __name__ == '__main__':
    param_dict["keywords"] = "  临海市"
    param_dict["subdistrict"] = 1
    param_dict["page"] = 1
    json_dict = getDistrict(**param_dict)
    print(json_dict)
