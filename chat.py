import streamlit as st
from agent import ConversationAgent, welcome_agent
from build_prompt import PromptMessage
from format_echarts import EchartsBuilder
from streamlit_echarts import st_pyecharts

st.title('🤖渠道积分AI助手😜')


# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

if "welcome_word" not in st.session_state:
    st.session_state.welcome_word = welcome_agent()
    st.session_state.messages.append({'role': 'assistant', 'content': st.session_state.welcome_word['text']})
    st.session_state.agent = ConversationAgent()
    st.session_state.agent.seed_agent()
    st.session_state.agent.generate_stage_analyzer(verbose=False)
    st.session_state.agent.generate_conversation_agent(verbose=True)
    st.session_state.agent.generate_echarts_chain(verbose=True)

    st.session_state.prom = PromptMessage()
    st.session_state.eb = EchartsBuilder()
    
    
if "introduc_msg" not in st.session_state: 
    st.session_state.introduc_msg = ["什么是渠道积分规则？","请帮我介绍一下主套餐积分规则？","帮我查询渠道结算积分？"]
       
if "stage_value" not in st.session_state:
    st.session_state.stage_value = ""

index = 0
# 展示聊天记录
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"], avatar='☺️'):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message(message["role"], avatar='🤖'):
            st.markdown(message["content"])
    elif message["role"] == "ec":
        ec_data = message["content"]
        if ec_data:
            with st.chat_message(message["role"], avatar='🤖'):
                index = index + 1
                st_pyecharts(key=index, chart = st.session_state.eb.build_chart(ec_data) ,height=500)



 
# 用于用户输入
if prompt := st.chat_input('我们来聊一点渠道积分相关的事儿吧'):
    with st.chat_message('user', avatar='😜'):
        st.markdown(prompt)
   

    st.session_state.messages.append({'role': 'user', 'content': prompt})
    # st.session_state.stage_value = st.session_state.agent.determine_conversation_stage(prompt)
    st.session_state.agent.human_step(prompt)
    response = st.session_state.agent.step()
    response_rdmp = st.session_state.agent.step_rdmp()

    with st.chat_message('assistant', avatar='🤖'):
        st.markdown(response)

    st.session_state.messages.append({'role': 'assistant', 'content': response})

    if response_rdmp:
        with st.chat_message('assistant', avatar='🤖'):
            st_pyecharts(st.session_state.eb.build_chart(response_rdmp),height=500)
        st.session_state.messages.append({'role': 'ec', 'content': response_rdmp})


    # 根据用户输入获取新的引导信息
    prm = st.session_state.prom.query_prompt(prompt)
    st.session_state.introduc_msg = prm["documents"][0]



# 展示引导信息
for introduc_msg in st.session_state.introduc_msg:
    if st.button(introduc_msg):
        st.session_state.messages.append({'role': 'user', 'content': introduc_msg})

        st.session_state.agent.human_step(introduc_msg)
        response = st.session_state.agent.step()
        response_rdmp = st.session_state.agent.step_rdmp()

        st.session_state.messages.append({'role': 'assistant', 'content': response})
        if response_rdmp:
            st.session_state.messages.append({'role': 'ec', 'content': response_rdmp})

        # 根据用户输入获取新的引导信息
        prm = st.session_state.prom.query_prompt(introduc_msg)
        st.session_state.introduc_msg = prm["documents"][0]

        st.experimental_rerun()  # 强制重新运行当前组件




