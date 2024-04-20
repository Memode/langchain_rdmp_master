import re
from typing import Union

from langchain.agents import Tool
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from typing import Callable
from langchain.prompts.base import StringPromptTemplate
from langchain.agents.agent import AgentOutputParser
from langchain.agents.conversational.prompt import FORMAT_INSTRUCTIONS
from langchain.schema import AgentAction, AgentFinish  # OutputParserException
from langchain.prompts import PromptTemplate
from build_knowlage import build_knowledge_base


def get_tools(knowledge_base):
    # we only use one tool for now, but this is highly extensible!
    tools = [
        Tool(
            name="RdmpRuleSearch",
            func=knowledge_base.invoke,
            description="如果用户查询和渠道积分规则相关的信息，使用该工具，包括查询渠道积分规则信息，输入应该是'请查询一下***渠道积分规则信息'",
        )
    ]
    print('tools构造正常')

    return tools

class CustomPromptTemplateForTools(StringPromptTemplate):
    # The template to use
    template: str

    tools_getter: Callable

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way

        intermediate_steps = kwargs.pop("intermediate_steps")

        thoughts = ""

        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value

        print('——thoughts——:'+thoughts+'\n End of ——thoughts——')

        kwargs["agent_scratchpad"] = thoughts

        tools = self.tools_getter([])


        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in tools]
        )
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in tools])

        print('prompt构造正常')

        return self.template.format(**kwargs)


class SalesConvoOutputParser(AgentOutputParser):
    ai_prefix: str = "AI"  # change for salesperson_name
    verbose: bool = True

    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        if self.verbose:
            print("TEXT")
            print(text)
            print("-------")

        if f"{self.ai_prefix}:" in text:
            if "Do I get the answer?YES." in text:
                print('判断Agent是否查到结果，yes')
                return AgentFinish(
                    {"output": text.split(f"{self.ai_prefix}:")[-1].strip()}, text)

            else:
                print('判断Agent是否查到结果，no')
                return AgentFinish({"output": {}}, text)


        regex = r"Action: (.*?)[\n]*Action Input: (.*)"
        match = re.search(regex, text)
        if not match:
            ## TODO - this is not entirely reliable, sometimes results in an error.
            return AgentFinish(
                {
                    "output": "I apologize, I was unable to find the answer to your question. Is there anything else I can help with?"
                },
                text,
            )
            # raise OutputParserException(f"Could not parse LLM output: `{text}`")
        action = match.group(1)
        action_input = match.group(2)

        print('output_paserser构造正常')
        return AgentAction(action.strip(), action_input.strip(" ").strip('"'), text)

    @property
    def _type(self) -> str:
        return "sales-agent"