from langchain_community.llms import Tongyi
from langchain.agents import initialize_agent

from myTools import getTools

if __name__ == '__main__':
    tools = getTools()
    llm = Tongyi()
    agent = initialize_agent(
        tools, llm, agent="zero-shot-react-description", verbose=True)


    # inputs =  "和渠道积分规则相关的信息"
    # response = agent.invoke({"input": inputs})
    # print(response)

    inputs = "请查询燕鸽湖手机专卖店NX.01.01.02.001.14的渠道酬金"
    response = agent.invoke({"input": inputs})
    print(response)