from typing import List

"""
金字塔处理
"""


class PyramidChart:
    @staticmethod
    def pyramid(data: List[dict], unit="", title: str = "", decimal_place: int = 2, **kwargs):
        """
        :param data: 数据，示例:[{"name":"上市企业","value":1}]
        :param unit: 数据单位
        :param title: 图题
        :param decimal_place: 小数点位数
        :param kwargs: 设置pool
        :return:
        """
        total = sum([_.get("value") for _ in data if _.get("value")])
        if total == 0:
            total = 1
        result = {
            "title": title,
            "series": [
                {
                    "name": title,
                    "data": [
                        {"name": item.get("name"), "value": item.get("value"),
                         "proportion": round(item.get("value", 0) / total * 100, decimal_place)} for item in data],
                    "unit": unit
                }
            ]
        }
        if kwargs:
            result["pool"] = kwargs

        return result
