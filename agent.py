from pydantic import Field
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain_community.llms import Tongyi
from langchain_core.output_parsers import StrOutputParser

from chain import StageAnalyzerChain, EchartsChain
from my_tools import *
from redis_tool import get_observation
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
    echarts_chain : EchartsChain = Field(...)
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

        ai_message = "AI:"+str(response["output"])
        self.conversation_history.append(ai_message)

        return ai_message.lstrip('AI:')

    def step_rdmp(self):
        rdmp_fx = get_observation()
        question = self.conversation_history[-2]
        history_text = self.conversation_history
        ec_message = ""
        if rdmp_fx is not None:
            echarts_data = self.echarts_chain.invoke({"input_text": rdmp_fx, "question": question, "chat_history": history_text})
            echarts_text = echarts_data["text"]
            start_index = echarts_text.find('{')
            end_index = echarts_text.rfind('}')
            ec_message = echarts_text[start_index:end_index+1]

        return ec_message

    def human_step(self,input_text):
        human_message = input_text
        human_message = "用户: " + human_message
        self.conversation_history.append(human_message)
        return human_message

    def generate_conversation_agent(self, verbose: bool = False):
        template = "{input}"
        tools = getTools()

        prompt = PromptTemplate.from_template(BASIC_TEMPLATE)
        # 构造输出转换器
        output_parser = StrOutputParser()
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
            handle_parsing_errors=True,
        )

        print("成功构造一个ConversationChain")

    def generate_stage_analyzer(self, verbose: bool = False):
        self.stage_analyzer_chain = EchartsChain.from_llm(
            llm=self.llm,
            verbose=verbose
        )

        print("成功构造一个StageAnalyzerChain")

    def generate_echarts_chain(self, verbose: bool = False):
        self.echarts_chain = EchartsChain.from_llm(
            llm=self.llm,
            verbose=verbose
        )

        print("成功构造一个EchartsChain")

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