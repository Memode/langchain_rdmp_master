from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from template import STAGE_ANALYZER_INCEPTION_PROMPT,BASIC_TEMPLATE,ECHARTS_PROMPT

class StageAnalyzerChain(LLMChain):
    """
        请针对 >>> 和 <<<中间的用户问题，选择一个合适的工具去回答它的问题。如果是A、B项，只要用A、B的选项字母告诉我答案。
        如果是C项，返回C选项，并且返回渠道NX编码值
        如果你觉得都不合适，就选D。
        >>>{history}<<<
        我们有的工具包括:
        A.闲聊，不需要选择工具工具
        B.一个能够解释渠道积分政策规则的工具
        C，一个能够查询渠道积分结算的工具
        D，都不合适
    """
    @classmethod
    def from_llm(cls, llm, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        stage_analyzer_inception_prompt_template = STAGE_ANALYZER_INCEPTION_PROMPT
        prompt = PromptTemplate(
            template=stage_analyzer_inception_prompt_template,
            input_variables=[
                "conversation_history",
                "question"
            ],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose, output_key="text")

class ConversationChain_Without_Tool(LLMChain):
    #当用户没有明确的感兴趣话题时，用这个chain和用户闲聊
    @classmethod
    def from_llm(cls, llm, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        conversation_without_tools_template = BASIC_TEMPLATE
        prompt = PromptTemplate(
            template=conversation_without_tools_template,
            input_variables=[
                "conversation_history",
            ],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)

class EchartsChain(LLMChain):
    """
    Task：你的任务是返回json数据
    Action：下面提供了三种图标的json格式，你需要将API返回的数据转换为其中的一种，其中type_name需要填充为当前数据主题，例如A渠道结算积分数据就是A渠道结算积分，以此类推
    Goal：只转换一种图表即可，请确保严格按照示例格式进行转换。
    """
    @classmethod
    def from_llm(cls, llm, verbose: bool = True)-> LLMChain:

        prompt = PromptTemplate(
            template=ECHARTS_PROMPT,
            input_variables=[
                "input_text",
                "question",
                "chat_history",
            ],
        )
        return cls(prompt=prompt, llm=llm, verbose=verbose)
