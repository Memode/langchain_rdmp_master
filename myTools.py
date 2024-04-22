import re

from langchain.tools import BaseTool
from build_knowlage import build_knowledge_base
from queryRdmpFx import queryRdmp


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
class queryRdmpFxTool(BaseTool):
    """
    一个帮助用户查询渠道结算积分信息的工具，并且能处理以下情况:
    1.在用户没有输入渠道名称或NX的渠道编码的的时候，会询问用户渠道名称和渠道NX编码
    2.在用户输入的渠道名称或NX的渠道编码查询不到的时候，会让用户二次确认渠道名称或NX的渠道编码是否正确
    """
    name = "queryRdmpFxTool"
    description = "如果用户查询渠道结算积分时，包括请查询***结算积分、请查询***渠道酬金等信息是，你必须使用这个工具进行查询"
    return_direct = False
    def _run(self, query: str) -> str:
        # 匹配多个数字以及大写字母
        pattern = r'NX.[a-zA-Z.0-9]+'
        match = re.findall(pattern, query)

        channel = query
        channel_code = ""
        channel_name = query


        if match:
            # 得到整个订单字符串
            channel_code = match[0]
            channel_name = channel.replace(channel_code, '')
        else:
            channel_code = None
            return "请问您的渠道NX编码是多少?"

        queryRdmpFx = queryRdmp(channel_name, channel_code)
        print("=========queryRdmpFx===============")
        return queryRdmpFx

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")

def getTools():
    # 将定义好的工具添加到工具包中
    # we only use one tool for now, but this is highly extensible!
    tools = [knowledgeTool(),queryRdmpFxTool()]
    print('tools构造正常')
    return tools


if __name__ == '__main__':
    getTools()