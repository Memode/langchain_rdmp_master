import json

from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts.charts import Line
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
#
# class bar:
#     def __init__(self, categories, name, data_list):
#         self.bar = [
#             {
#                 "chart_type": "bar",
#                 "data": {
#                     "categories": categories,
#                     "series": [
#                         {
#                             "name": name,
#                             "data": data_list
#                         }
#                     ]
#                 }
#             }
#         ]
#
# class line():
#     def __init__(self, categories, name, data_list):
#         self.line = [
#             {
#                 "chart_type": "line",
#                 "data": {
#                     "categories": categories,
#                     "series": [
#                         {
#                             "name": name,
#                             "data": data_list
#                         }
#                     ]
#                 }
#             }
#         ]

class EchartsBuilder:
    #
    # def general_json_builder(self, json_data:str):
    #     json_data = json.loads(json_data)
    #     for data in json_data:


    def build_chart(self, json_str):
        print(json_str, type(json_str))
        try:
            data = json.loads(json_str)

            try:
                # 尝试访问一个不存在的键
                self.x_axis = data["data"]["categories"]
            except KeyError:
                # 如果发生KeyError，执行以下代码
                self.x_axis = None

            try:
                self.y_axis = data["data"]["series"]
            except KeyError:
                self.y_axis = None

            try:
                self.chart_type = data["chart_type"]
            except KeyError:
                self.chart_type = None



            if self.chart_type.lower() == "bar":
                return self.build_bar_chart()
            if self.chart_type.lower() == "line":
                return self.build_line_chart()
            if self.chart_type.lower() == "pie":
                return self.build_pie_chart()
        except KeyError:
            return None

    def build_bar_chart(self):
        bar = Bar()
        bar.add_xaxis(self.x_axis)
        for data in self.y_axis:
            bar.add_yaxis(data.get("name"), data.get("data"))
        return bar

    def build_line_chart(self):
        line = Line()
        line.add_xaxis(self.x_axis)
        for data in self.y_axis:
            line.add_yaxis(data.get("name"), data.get("data"))
        return line

    def build_pie_chart(self):
        pie = Pie()
        # # # 向饼图添加数据
        pie.add("", json_to_tuple_set(json.dumps(self.y_axis)), radius=['20%', '60%'])


        # 设置全局选项
        pie.set_global_opts(
            title_opts={'text': '渠道结算积分','center': 'center'},  # 标题文本和位置
            legend_opts={'bottom': 'bottom'},  # 图例布局方向和位置
        )

        # 设置系列配置项，控制标签的显示
        pie.set_series_opts(
            label_opts={
                'show': False  # 隐藏标签
            }
        )
        return pie

def json_to_tuple_set(json_str :str):
    data = json.loads(json_str)
    # 确认 data 是一个列表
    if not isinstance(data, list): # 输出：True
        raise ValueError("JSON must represent a list of elements")
    # 访问列表中的元素
    tuple_list = [(d["name"],d["value"]) for d in data]

    return tuple_list


if __name__ == "__main__":
    json_data0 = '''
        {
          "chart_type": "bar",
          "data": {
            "categories": ["202401", "202402", "202403", "202404"],
            "series": [
              {
                "name": "兴庆区燕鸽湖手机专卖店（邵勇）结算积分",
                "data": [12340.1, 19787.73, 9075.02, 4622.89]
              }
            ]
          }
        }

    '''

    json_data1 = '''
        {
        "chart_type": "line",
        "data": {
            "categories": ["category1", "category2", "category3"],
            "series": [
                    {
                    "name": "兴庆区燕鸽湖手机专卖店（邵勇）",
                    "data": [10, 15, 20]
                    }
                ]
            }
        }
    '''

    json_data2 = '''
        {
          "chart_type": "pie",
          "data": {
            "series": [
              {"name": "终端结算积分", "value": 140},
              {"name": "主套餐新增结算积分", "value": 918.5},
              {"name": "主套餐迁转结算积分", "value": 62.26},
              {"name": "家宽业务裸宽结算积分", "value": 10},
              {"name": "家宽业务融合结算积分", "value": 104.1},
              {"name": "业务办理服务费结算积分", "value": 20},
              {"name": "业务办理手续费结算积分", "value": 3},
              {"name": "权益及新业务结算积分", "value": 152},
              {"name": "流量结算积分", "value": 10.5},
              {"name": "政企业务结算积分", "value": 0},
              {"name": "代收费结算积分", "value": 10.6},
              {"name": "激励费用结算积分", "value": 80.0},
              {"name": "精准营销结算积分", "value": 80},
              {"name": "结算积分合计", "value": 1590.26}
            ]
          }
        }

    '''



if __name__ == '__main__':
    astr = """
    {
  "chart_type": "bar",
  "data": {
    "categories": [
      "终端结算积分",
      "主套餐新增结算积分",
      "主套餐迁转结算积分",
      "家宽业务裸宽结算积分",
      "家宽业务融合结算积分",
      "业务办理服务费结算积分",
      "业务办理手续费结算积分",
      "智家结算积分",
      "权益及新业务结算积分",
      "大屏结算积分",
      "流量结算积分",
      "政企业务结算积分",
      "代收费结算积分",
      "合约结算积分",
      "激励费用结算积分",
      "上月负值递延结算积分",
      "小额酬金调剂结算积分",
      "精准营销结算积分"
    ],
    "series": [
      {
        "name": "NX.01.01.02.001.14 当月详细结算积分",
        "data": [
          A036,
          A048,
          A057,
          A076,
          A087,
          A096,
          A103,
          A112,
          A120,
          A128,
          A138,
          A147,
          A156,
          A161,
          A171,
          A172,
          A173,
          A182
        ]
      }
    ]
  }
}

    """
    ec = EchartsBuilder()
    st_pyecharts(ec.build_chart(astr), height=500)



