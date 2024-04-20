import streamlit as st
from agent import ConversationAgent, welcome_agent
from build_prompt import PromptMessage


st.title('🤖渠道积分AI机器人😜')

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

  
               
if "welcome_word" not in st.session_state:
    st.session_state.welcome_word = welcome_agent()
    st.session_state.messages.append({'role': 'assistant', 'content': st.session_state.welcome_word['text']})
    st.session_state.agent = ConversationAgent()
    st.session_state.agent.seed_agent()
    st.session_state.agent.generate_stage_analyzer(verbose=True)
    st.session_state.prom = PromptMessage()
    
    
if "introduc_msg" not in st.session_state: 
    st.session_state.introduc_msg = ["什么是渠道积分规则？","请帮我介绍一下主套餐积分规则？","帮我查询渠道结算积分？"]
       

# 展示聊天记录
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"], avatar='☺️'):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"], avatar='🤖'):
            st.markdown(message["content"])
            

 
# 用于用户输入
if prompt := st.chat_input('我们来聊一点旅游相关的事儿吧'):
    with st.chat_message('user', avatar='😜'):
        st.markdown(prompt)
   

    st.session_state.messages.append({'role': 'user', 'content': prompt})
    # st.session_state.agent.determine_conversation_stage(prompt)
    st.session_state.agent.human_step(prompt)
    response = st.session_state.agent.step()
   

    with st.chat_message('assistant', avatar='🤖'):
        st.markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
    
    # 根据用户输入获取新的引导信息
    prm = st.session_state.prom.query_prompt(prompt)
    st.session_state.introduc_msg = prm["documents"][0]

    
# 展示引导信息
for introduc_msg in st.session_state.introduc_msg:
    if st.button(introduc_msg):
        st.session_state.messages.append({'role': 'user', 'content': introduc_msg})
        # st.session_state.agent.determine_conversation_stage(introduc_msg)
        st.session_state.agent.human_step(introduc_msg)
        response = st.session_state.agent.step()
        st.session_state.messages.append({'role': 'assistant', 'content': response})

        # 根据用户输入获取新的引导信息
        prm = st.session_state.prom.query_prompt(introduc_msg)
        st.session_state.introduc_msg = prm["documents"][0]
        st.experimental_rerun()  # 强制重新运行当前组件

    