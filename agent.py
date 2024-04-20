from typing import Any, Callable, Dict, List, Union
import streamlit as st

from pydantic import Field
# from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import LLMSingleActionAgent,AgentExecutor
from langchain.agents import AgentExecutor,Tool,ZeroShotAgent
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent

from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.llms.chatglm3 import ChatGLM3
from langchain_community.llms import Tongyi

from chain import StageAnalyzerChain,ConversationChain_Without_Tool
from my_tools import *
from stages import *
from myTools import *
from template import *

def welcome_agent():
    template = "{input}"
    prompt = PromptTemplate.from_template(WELCOME_TEMPLATE)

    endpoint_url = "http://127.0.0.1:8000/v1/chat/completions"
    # llm = ChatGLM3(
    #     endpoint_url=endpoint_url,
    #     max_tokens=4096,
    #     # prefix_messages=messages,
    #     top_p=0.9
    # )

    llm = Tongyi()
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.invoke({"input": "简短的欢迎词"})

    return response


def fake_system():
    fake_message = {'text':'模拟输出'}
    return fake_message

class ConversationAgent():
    stage_analyzer_chain: StageAnalyzerChain = Field(...)
    conversation_agent_without_tool = Field()
    conversation_agent_with_tool = Field()

    conversation_history = []
    conversation_stage_id: str = "1"
    current_conversation_stage: str = CONVERSATION_STAGES.get("1")
    
    template = "{input}"
    prompt = PromptTemplate.from_template(BASIC_TEMPLATE)

    endpoint_url = "http://127.0.0.1:8000/v1/chat/completions"
    # llm = ChatGLM3(
    #     endpoint_url=endpoint_url,
    #     max_tokens=4096,
    #     # prefix_messages=messages,
    #     top_p=0.9
    # )
    llm = Tongyi()
    
    def seed_agent(self):
        self.conversation_history.clear()
        print("——Seed Successful——")

    def show_chat_history(self):
        return self.conversation_history

    def retrieve_conversation_stage(self, key):
        return CONVERSATION_STAGES.get(key)

    def fake_step(self):
        input_text = self.conversation_history[-1]
        ai_message = self._respond_with_tools(str(input_text), verbose=True)
        print(ai_message,type(ai_message['output']))

    def step(self):
        input_text = self.conversation_history[-1]
        # print(str(input_text)+'input_text****')

        
        # ai_message = self._respond_without_tools(str(input_text), verbose=True)

        # if int(self.conversation_stage_id) == 0:
        #     ai_message = self._respond_without_tools(str(input_text),verbose=True)
        # elif int(self.conversation_stage_id) == 1:
        #     ai_message = self._respond_without_tools(str(input_text),verbose=True)
        # else:
        #     ai_message = self._respond_without_tools(str(input_text), verbose=True)

        recommend_message = self._respond_with_tool(input_text)
        print(recommend_message, len(recommend_message))
        # print(ai_message,type(ai_message))
        ai_message = "AI:"+str(recommend_message)
        # ai_message = "AI:"+str(ai_message)
        self.conversation_history.append(ai_message)
        # print(f"——系统返回消息'{ai_message}'，并添加到history里——")
        return ai_message.lstrip('AI:')

    
    def human_step(self,input_text):
        human_message = input_text
        human_message = "用户: " + human_message
        self.conversation_history.append(human_message)
        # print(f"——用户输入消息'{human_message}'，并添加到history里——")
        return human_message

    def generate_stage_analyzer(self,verbose: bool = False):
        self.stage_analyzer_chain = StageAnalyzerChain.from_llm(
            llm=self.llm,
            verbose=verbose
        )

        print("成功构造一个StageAnalyzerChain")


    def determine_conversation_stage(self,question):
        self.question = question
        print('-----进入阶段判断方法-----')
        self.conversation_stage_id = self.stage_analyzer_chain.run(
            conversation_history=self.conversation_history,
            question=self.question
        )

        print(f"Conversation Stage ID: {self.conversation_stage_id}")
        print(type(self.conversation_stage_id))
        self.current_conversation_stage = self.retrieve_conversation_stage(
            self.conversation_stage_id
        )
        print(f"Conversation Stage: {self.current_conversation_stage}")

    def _respond_without_tools(self,input_text,verbose: bool = False):
        self.conversation_agent_without_tool = ConversationChain_Without_Tool.from_llm(
            llm=self.llm,
            verbose=verbose
        )

        response = self.conversation_agent_without_tool.run(
            question = input_text,
            conversation_history=self.conversation_history,
        )

        return response
    def get_tools(self):
        file_path = r'./categories'
        knowledge_base = build_knowledge_base(file_path)
        tools = get_tools(knowledge_base)
        return tools


    def recommend_product(self, inputs, verbose =True):

        tools = self.get_tools()

        prompt = CustomPromptTemplateForTools(
            template=RECOMMEND_TEMPLATE,
            tools_getter=lambda x: tools,
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=[
                "intermediate_steps",  # 这是在调用tools时，会产生的中间变量，是一个list里面的一个tuple，一个是action，一个是observation
                "conversation_history",
            ],
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt, verbose=verbose)

        tool_names = [tool.name for tool in tools]

        # WARNING: this output parser is NOT reliable yet
        ## It makes assumptions about output from LLM which can break and throw an error
        output_parser = SalesConvoOutputParser()

        recommend_agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names,

        )

        sales_agent_executor = AgentExecutor.from_agent_and_tools(
            agent=recommend_agent, tools=tools, verbose=verbose, max_iterations=5
        )

        # inputs = {
        #     "conversation_history": "\n".join(self.conversation_history),
        # }

        response = sales_agent_executor.invoke(inputs)

    def _respond_with_tool(self, inputs, verbose=True):
        tools = getTools()
        agent = initialize_agent(
            tools,
            self.llm,
            agent="zero-shot-react-description",
            verbose=verbose)

        response = agent.invoke({"input": inputs})
        return str(response['output'])









