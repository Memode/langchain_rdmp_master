from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from pydantic import Field
from langchain.prompts import PromptTemplate
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.tools.render import format_tool_to_openai_function
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain_community.llms import Tongyi
from langchain_core.output_parsers import StrOutputParser

from chain import StageAnalyzerChain
from myTools import *
from stages import CONVERSATION_STAGES
from template import *

def welcome_agent():
    prompt = PromptTemplate.from_template(WELCOME_TEMPLATE)

    # endpoint_url = "http://127.0.0.1:8000/v1/chat/completions"
    # llm = ChatGLM3(
    #     endpoint_url=endpoint_url,
    #     max_tokens=4096,
    #     # prefix_messages=messages,
    #     top_p=0.9
    # )

    llm = Tongyi()
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.invoke({"input": "简短的欢迎词"})
    # response = "欢迎光临"
    return response



def fake_system():
    fake_message = {'text':'模拟输出'}
    return fake_message

class ConversationAgent():
    stage_analyzer_chain: StageAnalyzerChain = Field(...)
    conversation_agent = None
    conversation_history = []
    conversation_stage_id: str = "A"
    current_conversation_stage: str = CONVERSATION_STAGES.get("A")
    endpoint_url = "http://127.0.0.1:8000/v1/chat/completions"
    max_tokens = 4096

    llm = None

    def __init__(self):
        # llm = ChatGLM3(
        #     endpoint_url=self.endpoint_url,
        #     max_tokens=self.4096,
        #     # prefix_messages=messages,
        #     top_p=0.9
        # )

        self.llm = Tongyi()

    def seed_agent(self):
        self.conversation_history.clear()
        print("——Seed Successful——")

    def show_chat_history(self):
        return self.conversation_history


    def step(self):
        input_text = self.conversation_history[-1]
        response = self.conversation_agent.invoke({"input": input_text})
        print(response)

        ai_message = "AI:"+str(response["output"])
        self.conversation_history.append(ai_message)
        return ai_message.lstrip('AI:')

    
    def human_step(self,input_text):
        human_message = input_text
        human_message = "用户: " + human_message
        self.conversation_history.append(human_message)
        return human_message

    def generate_conversation_agent(self, verbose: bool = False):
        template = "{input}"
        human_message_template = HumanMessagePromptTemplate.from_template(BASIC_TEMPLATE)

        prompt = ChatPromptTemplate.from_messages(
            [MessagesPlaceholder(variable_name="conversation"), human_message_template]
        )
        # 构造输出转换器
        output_parser = StrOutputParser()



        tools = getTools()

        llm_with_tools = self.llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=False, verbose=verbose)
        # 更改agent为conversational-react-description支持多语言对话
        self.conversation_agent = initialize_agent(
            tools,
            self.llm,
            agent="conversational-react-description",
            memory=memory,
            verbose=verbose,
            output_parser=output_parser,
            prompt=prompt,
            llm_with_tools=llm_with_tools,
            OpenAIFunctionsAgentOutputParser=OpenAIFunctionsAgentOutputParser,
        )

        print("成功构造一个ConversationChain")

    def generate_stage_analyzer(self, verbose: bool = False):
        self.stage_analyzer_chain = StageAnalyzerChain.from_llm(
            llm=self.llm,
            verbose=verbose
        )

        print("成功构造一个StageAnalyzerChain")

    def determine_conversation_stage(self, question):
        self.question = question
        print('-----进入阶段方法-----')
        print(str(self.conversation_history)+":"+self.question)
        self.conversation_stage_id = self.stage_analyzer_chain.invoke(
            {"chat_history": self.conversation_history,
            "question":self.question,
            }
        )

        print(f"Conversation Stage ID: {self.conversation_stage_id}")
        print(type(self.conversation_stage_id["text"]))
        self.current_conversation_stage = self.retrieve_conversation_stage(
            self.conversation_stage_id["text"]
        )
        print(f"Conversation Stage: {self.current_conversation_stage}")
        return  self.conversation_stage_id["text"]

    def retrieve_conversation_stage(self, key = "A"):
        return CONVERSATION_STAGES.get(key)