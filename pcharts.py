import random

import streamlit as st
import numpy as np
import pandas as pd
from pyecharts.charts import Bar, Line, Pie
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts,st_echarts


def get_bar_chart():
    # 创建一个条形图
    bar = (
        Bar()
        .add_xaxis(["A", "B", "C", "D", "E", "F"])
        .add_yaxis("Series 1", [10, 20, 30, 40, 50, 60])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar Chart"))
    )

    # 将条形图嵌入到Streamlit应用中
    st_pyecharts(bar)


def render_basic_line_chart():
    option = {
        "xAxis": {
            "type": "category",
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {"type": "value"},
        "series": [{"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}],
    }
    st_echarts(
        options=option, height="400px",
    )


def render_basic_2line_chart():
    columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    line = Line().add_xaxis(columns)

    line.width = '1000px'
    data1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
    data2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
    line.add_yaxis(series_name="降水量", y_axis=data1, label_opts=opts.LabelOpts(is_show=True))
    line.add_yaxis(series_name="蒸发量", y_axis=data2, label_opts=opts.LabelOpts(is_show=True))

    st_pyecharts(line)

def render_basic_pie_chart():
    option = {
        "title": {
            "text": 'Referer of a Website',
            "subtext": 'Fake Data',
            "left": 'center'
        },
        "tooltip": {
            "trigger": 'item'
        },
        "legend": {
            "orient": 'vertical',
            "left": 'left'
        },
        "series": [
            {
                "name": 'Access From',
                "type": 'pie',
                "radius": '50%',
                "data": [
                    {"value": 1048, "name": 'Search Engine'},
                    {"value": 735, "name": 'Direct'},
                    {"value": 580, "name": 'Email'},
                    {"value": 484, "name": 'Union Ads'},
                    {"value": 300, "name": 'Video Ads'}
                ],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    # 将饼图添加到Streamlit页面
    st_echarts(options=option)


def render_basic_table_chart():
    random_data = np.random.rand(10, 10)
    df = pd.DataFrame(random_data, columns=[f'Col{i}' for i in range(1, 11)])
    st.dataframe(df)

def get_chart():
    rd = random.randint(1,5)
    if rd == 1:
        render_basic_line_chart()
    elif rd == 2:
        render_basic_2line_chart()
    elif rd == 3:
        get_bar_chart()
    elif rd == 4:
        render_basic_table_chart()
    else:
        render_basic_pie_chart()