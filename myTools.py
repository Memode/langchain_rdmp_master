from langchain.tools import BaseTool

from build_knowlage import build_knowledge_base
from queryRdmpFx import queryRdmp


# 搜索工具
class knowledgeTool(BaseTool):
    name = "knowledgeTool"
    description = "如果用户查询和渠道积分规则相关的信息，包括查询什么是渠道积分规则、主套餐、家宽、终端、流量、新业务等积分规则相关的知识请使用该工具"
    return_direct = False  # 直接返回结果
    def _run(self, query: str) -> str:
        retrieverTool = build_knowledge_base(directory="categories")
        return retrieverTool.invoke(query)
    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")


class queryRdmpFxTool(BaseTool):
    name = "queryRdmpFxTool"
    description = "如果用户查询渠道结算积分时，包括请查询***结算积分、请查询***渠道酬金等信息是，你必须使用这个工具进行查询"
    return_direct = False
    def _run(self, query: str) -> str:
        queryRdmpFx = queryRdmp(query)
        return queryRdmpFx

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")

def getTools():
    # 将定义好的工具添加到工具包中
    # we only use one tool for now, but this is highly extensible!
    tools = [knowledgeTool(),queryRdmpFxTool()]
    print('tools构造正常')
    return tools
