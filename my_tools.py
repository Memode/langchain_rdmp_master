import json
import re
from typing import Union,Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta

from langchain.tools import BaseTool
from build_knowlage import build_knowledge_base
from query_rdmpfx import queryRdmp, query_rdmpfx
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from redis_tool import set_observation


# 搜索工具
class knowledgeTool(BaseTool):
    """如果用户查询和渠道积分规则相关的信息，包括查询什么是渠道积分规则、主套餐、家宽、终端、流量、新业务等积分规则相关的知识请使用该工具"""
    name = "knowledgeTool"
    description = "如果用户查询和渠道积分规则相关的信息，包括查询什么是渠道积分规则、主套餐、家宽、终端、流量、新业务等积分规则相关的知识请使用该工具"
    return_direct = False  # 直接返回结果
    def _run(self, query: str) -> str:
        retrieverTool = build_knowledge_base(directory="categories")
        return retrieverTool.invoke(query)
    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")

# 分项信息查询
class queryRdmpFxTool1(BaseTool):

    """
    一个帮助用户查询渠道结算积分信息的工具，并且能处理以下情况:
    1.在用户没有输入渠道名称或NX的渠道编码的的时候，会询问用户渠道名称和渠道NX编码
    2.在用户输入的渠道名称或NX的渠道编码查询不到的时候，会让用户二次确认渠道名称或NX的渠道编码是否正确
    """
    name = "queryRdmpFxTool"
    description = "如果用户查询渠道结算积分时，包括请查询***结算积分、请查询***渠道酬金等信息是，你必须使用这个工具进行查询"
    return_direct = False

    def _run(self, query: str,  run_manager: Optional[CallbackManagerForToolRun] = None) -> str:

        # 匹配多个数字以及大写字母
        pattern = r'NX.[a-zA-Z.0-9]+'
        match = re.findall(pattern, query)

        channel = query
        channel_code = ""
        channel_name = query
        # 获取当前日期
        today = datetime.today()
        months_ago = today - relativedelta(month=1)
        # 格式化日期为 yyyymm
        month_begin = months_ago.strftime('%Y%m')
        month_end = today.strftime('%Y%m')

        if match:
            # 得到整个订单字符串
            channel_code = match[0]
            channel_name = channel.replace(channel_code, '')
        else:
            channel_code = None

            return "请问您的渠道NX编码是多少?"
        if channel_code:
            channel_name = None

        queryRdmpFx = queryRdmp(channel_name, channel_code, month_begin, month_end)
        set_observation(queryRdmpFx=str(queryRdmpFx))
        return queryRdmpFx



    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("暂时不支持异步")


# 分项信息查询
class queryRdmpFxTool(BaseTool):

    """
    一个帮助用户查询渠道结算积分信息的工具，并且能处理以下情况:
    1.在用户没有输入渠道名称或NX的渠道编码的的时候，会询问用户渠道名称和渠道NX编码
    2.在用户输入的渠道名称或NX的渠道编码查询不到的时候，会让用户二次确认渠道名称或NX的渠道编码是否正确
    3.在用户输入的查询当月、近三月、半年、近一年或者具体到2024年12月等日期时间的，自动转换为YYYYMM格式的字符串数据，并且标记为bging_month:202302,end_month:202303，传送到工具中
    """
    name = "queryRdmpFxTool"
    description = ("如果用户查询渠道结算积分时，包括请查询***结算积分、请查询***渠道酬金等信息是，你必须使用这个工具进行查询"
    "use this tool inputs are multi parameters,need multi input variables,like the nx_code,token,chat_history."
    "To use the tool, you must provide at least three of the following parameters "
    "['nxcode', 'token','chat_history'].")
    return_direct = False

    def _run(self, input: Optional[Union[str,str,str]]) -> str:
        input_json = json.loads(input)
        print(input_json,type(input_json))
        nx_code = input_json["nx_code"]
        token = input_json["token"]
        chat_history = input_json["chat_history"]


        # 匹配多个数字以及大写字母
        pattern = r'NX.[a-zA-Z.0-9]+'
        match = re.findall(pattern, nx_code)
        channel = nx_code
        channel_code = ""
        channel_name = nx_code

        if match:
            # 得到整个订单字符串
            channel_code = match[0]
            channel_name = channel.replace(channel_code, '')
        else:
            channel_code = None

            return "请问您的渠道NX编码是多少?"
        if channel_code:
            channel_name = None


        queryRdmpFx = query_rdmpfx(query=channel_code,token=token,chat_history=chat_history)
        return queryRdmpFx
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("暂时不支持异步")

def getTools():
    # 将定义好的工具添加到工具包中
    # we only use one tool for now, but this is highly extensible!
    tools = [knowledgeTool(),queryRdmpFxTool()]
    print('tools构造正常')
    return tools


# if __name__ == '__main__':
#     getTools()

