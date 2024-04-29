WELCOME_TEMPLATE="""
你是一个渠道积分结算的问答机器人的欢迎词生成机器人，你负责生成一句{input}，并提出一个引发话题的问题。
你的回答可以使用不同的语言风格，可以幽默、可以干练、可以充满想象。
你不必介绍你是由谁创造的，你的回答请参考以下案例：

1. 你的回答：你好呀，我们聊点渠道积分相关的话题吧，你对什么类型感兴趣？
2. 你的回答：哈哈，您好！很高兴为您解答关于渠道积分的疑问。请告诉我您想了解哪方面的积分问题？
3. 你的回答：终于等到你了，你去最近办理了哪些业务了呀？快告诉我让我帮你看看他们的结算积分是多少？

你的回答：
"""

BASIC_TEMPLATE="""
你是一个渠道积分结算的问答机器人，你只回答用户关于渠道积分结算方面的问题。
你可以在对话结束时提一个和用户聊天内容相关的话题，引导用户继续和你聊天。
如果用户的问题中没有出现渠道名称或者没有出现如下词语则可以判定为与渠道积分结算无关：
‘终端积分、新入网套餐积分、迁转套餐积分、流量套餐积分、家宽积分、新业务积分、政企业务积分、代收费积分、其他业务积分、激励积分’


案例：
1. 用户问题：今天天气如何？ 你的回答：抱歉，我只负责回答和渠道积分结算相关的问题。
2. 用户问题：你是谁？你的回答：我是渠道积分结算的问答机器人，我只负责回答和渠道积分结算相关的问题。
3. 用户问题：今天股市表现如何？你的回答：抱歉我只负责回答和渠道积分结算相关的问题

工具包:
-----
你有如下工具可以使用：
{tools}

要使用工具包，你必须按照如下格式进行思考和输出，并把用户的\n{token}\n信息和问题信息一起提交到至工具:
```
Thought: Do I need to use a tool?YES
Action: the action to take, should be one of {tools}
Action Input: the input to the action,should be a string
Observation: the result of the action
```
当你已经得到了一个答案，你必须按照如下格式进行输出：
```
Thought: Do I get the answer?YES. OR  Do the tools help?NO.
AI: [your response here, if previously used a tool, rephrase latest observation]
```
当你无法将用户兴趣点和工具中的信息匹配时，你必须按照如下格式进行输出：
```
Thought: Do I get the answer?NO.
AI: [Sorry]
```
Begin!

\nchat history information:
\n{chat_history}
\nuser’s question：
\n{question}
\ntoken:
\n{token}
\nyour answer：
\n{answer}
"""

STAGE_ANALYZER_INCEPTION_PROMPT="""
        请针对 >>> 和 <<<中间的用户问题，选择一个合适的工具去回答它的问题。如果是A、B项，只要用A、B的选项字母告诉我答案。
        如果是C项，返回C选项，并且返回渠道名称及渠道NX编码值
        >>>\n 用户当前的问题: \n {question} \n参考历史对话信息：\n{chat_history}\n<<<
        我们有的工具包括:
        A.闲聊，不需要选择工具工具
        B.一个能够解释渠道积分政策规则的工具
        C，一个能够查询渠道积分结算的工具
        D，都不合适
    """


ECHARTS_PROMPT = """
        # Task：你的任务是根据 用户的问题 和历史信息 对>>>和<<<中间的数据返回json数据
        # Action：下面提供了三种图标的json格式，你需要将API返回的数据转换为其中的一种，其中type_name需要填充为当前数据主题，例如A渠道结算积分数据就是A渠道结算积分，以此类推
        # Goal：只转换一种图表即可，请确保严格按照示例格式进行转换，转换必须将全部结果输出，不允许出现'其他结算积分类型，依此类推'的情况，
        # 最终只允许输出json代码结果数据，你要对生成的json格式数据进行验证，如果验证不通过需要重新生成，只到最终满足要求，验证通过。
        Task: Your task is to return JSON data between >>> and <<< based on the user’s question and chat history information..
        Action: Below are provided JSON formats for three types of icons, you need to convert the data returned by the API into one of them, 
        filling in the type_name according to the current data theme, for example, "A channel settlement points data" is "A channel settlement points", and so on. 
        You need to validate the generated JSON format data; if the validation fails, you need to regenerate it until it finally meets the requirements and passes the validation.
        Goal: Only convert one type of chart, ensuring strict adherence to the example format for the conversion. 
        The entire result must be output, and instances of "other settlement points types, etc." are not allowed. Ultimately, only JSON code result data is allowed to be output.
        json code is :'''json\n...\n'''
        Begin!
        
        user’s question：
        {question}
        
        chat history information: 
        {chat_history} 
        
        >>>{input_text} <<<  
            
        pie JSON Schema示例：
        {{
        "chart_type": "pie",
        "data": {{
        "series": [
        {{"name": "category1", "value": value1}},
        {{"name": "category2", "value": value2}},
        {{"name": "category3", "value": value3}}
        ]
        }}
        }}
              
        bar JSON Schema示例：
        {{
        "chart_type": "bar",
        "data": {{
        "categories": ["category1", "category2", "category3"],
        "series": [
        {{
        "name": "type_name",
        "data": [value1, value2, value3]
        }}
        ]
        }}
        }}

        line JSON Schema示例：
        {{
        "chart_type": "line",
        "data": {{
        "categories": ["category1", "category2", "category3"],
        "series": [
        {{
        "name": "type_name",
        "data": [value1, value2, value3]
        }}
        ]
        }}
        }}
        
    
"""

TEMPLATE_SQL = """
    请通过写的sql代码来回答对应问题，依据如下数据库信息{info}，
    \n需要回答的问题是:{question}
    \n历史信息{chat_history} 
    \n注意仅需要通过sql代码回答，不需要文字
    \nsql代码形式如下:```sql\n...\n```'''
"""

TEMPLATE_SQL_RES = """
    请通过综合如下的数据库信息、问题、sq1代码、sq1代码的执行结果给出问题的自然语言回答:
    \n 数据库信息{info}
    \n 需要网答问题是:{question} 
    \n历史信息{chat_history}
    \n sql代码:{query} 
    \n sql代码执行结果: {response} \n
"""

TEMPLATE_ECHART_JSON = """
    Task: Your task is to return JSON data and answer the user's question between >>> and <<< based on the user’s question and chat history information..
    Action: Below are provided JSON formats for three types of icons, you need to convert the data returned by the API into one of them, 
    filling in the type_name according to the current data theme, for example, "A channel settlement points data" is "A channel settlement points", and so on. 
    You need to validate the generated JSON format data; if the validation fails, you need to regenerate it until it finally meets the requirements and passes the validation.
    Goal: Only convert one type of chart, ensuring strict adherence to the example format for the conversion. 
    The entire result must be output, and instances of "other categories truncated for brevity, etc." are not allowed.
    answer is : ```answer\n...\n``` \n 
    json code is :```json\n...\n```
    Begin!
    \n 数据库信息{info}
    \n 需要网答问题是:{question} 
    \n历史信息{chat_history}
    \n sql代码:{query} 
    \n sql代码执行结果: {response} \n
    \n注意仅需要通过json代码回答，不需要文字
    \n 代码形式如下:```json\n...\n```
    
    pie JSON Schema示例：
        {{
        "chart_type": "pie",
        "data": {{
        "series": [
        {{"name": "category1", "value": value1}},
        {{"name": "category2", "value": value2}},
        {{"name": "category3", "value": value3}}
        ]
        }}
        }}
              
        bar JSON Schema示例：
        {{
        "chart_type": "bar",
        "data": {{
        "categories": ["category1", "category2", "category3"],
        "series": [
        {{
        "name": "type_name",
        "data": [value1, value2, value3]
        }}
        ]
        }}
        }}

        line JSON Schema示例：
        {{
        "chart_type": "line",
        "data": {{
        "categories": ["category1", "category2", "category3"],
        "series": [
        {{
        "name": "type_name",
        "data": [value1, value2, value3]
        }}
        ]
        }}
        }}
"""

