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
    description = ("如果用户查询和渠道积分规则相关的信息，包括查询什么是渠道积分规则、主套餐、家宽、终端、流量、新业务等积分规则相关的知识请使用该工具"
                   """.use this tool inputs are multi parameters,need multi input variables,like the {{"input_text":"user questions", "token":"token"}}."""
                   """.To use the tool, you must provide at least three of the following parameters and history message """)
    return_direct = False  # 直接返回结果
    def _run(self, query: str) -> str:
        print("*"*5,query)
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
    """一个帮助用户查询渠道结算积分信息的工具，并且能处理以下情况:
                        如果用户查询渠道结算积分时，包括请查询***结算积分、请查询***渠道酬金等信息是，你必须使用这个工具进行查询
                       1.在用户没有输入渠道名称或NX的渠道编码的的时候，会询问用户渠道名称和渠道NX编码
                       2.在用户输入的渠道名称或NX的渠道编码查询不到的时候，会让用户二次确认渠道名称或NX的渠道编码是否正确
                       """
    name = "queryRdmpFxTool"
    description = ("""一个帮助用户查询渠道结算积分信息的工具，并且能处理以下情况:"""
                   """.use this tool inputs are multi parameters,need multi input variables,like the {{"nxcode":"value1", "token":"value2","input_text":"value3"}}."""
                   """.To use the tool, you must provide at least three of the following parameters and history message """
                   # """.参数必须严格按照json格式提供：\n{{"nxcode":"NX.01", "token":"token","input_text":"history message"}}"""
                   )
    return_direct = False

    # def _run(self, input: Optional[Union[str,str,str]]) -> str:
    def _run(self, input: str) -> str:

        # 匹配多个数字以及大写字母
        pattern = r'NX.[a-zA-Z.0-9]+'
        match = re.findall(pattern, input)

        if match:
            # 得到整个订单字符串
            channel_code = match[0]
            result_dict = json.loads(input.replace("'", "\""))

            try:
                nxcode = result_dict["nxcode"]
                token = result_dict["token"]
            except KeyError:
                return "请问您的渠道NX编码是多少?"

            try:
                input_text = result_dict["input_text"]
            except KeyError:
                input_text = "查询渠道近三月结算积分"
        else:
            return "请问您的渠道NX编码是多少?"

        queryRdmpFx = query_rdmpfx(query=nxcode,token=token,chat_history=input_text)
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

