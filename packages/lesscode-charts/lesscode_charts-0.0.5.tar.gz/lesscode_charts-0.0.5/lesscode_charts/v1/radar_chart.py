from typing import List

"""
雷达图
"""


class RadarChart:
    @staticmethod
    def radar(indicator_list: List[str], data_list: List[dict], title: str, unit_list: List[str]):
        """
        :param indicator_list: 指标列表
        :param data_list: 数据，value字段为列表
        :param title: 图题
        :param unit_list: 单位列表
        :return:
        """
        result = {
            "indicator": indicator_list,
            "series": [
                {
                    "name": title,
                    "data": [
                        {"name": item.get("name"), "value": item.get("value", [])} for item in data_list
                    ],
                    "unit": unit_list
                }
            ],
            "title": title
        }
        return result
