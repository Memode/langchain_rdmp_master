# from my_tools import build_knowledge_base
#
# file_path = r'C:\Users\Administrator\langchain_chatbot\product.txt'
# knowledge_base = build_knowledge_base(file_path)
# answer = knowledge_base.invoke('请介绍一下上海的旅游产品')
# print(answer)
from langchain_community.llms.chatglm3 import ChatGLM3
from langchain_core.prompts import PromptTemplate
import requests
from openai import OpenAI
import math
import uuid
import base64
import hashlib
import json
import time
from datetime import datetime

from redis_tool import *

# from agent import ConversationAgent,welcome_agent
#
# agent = ConversationAgent()
# print(dir(ConversationAgent))
# # agent.seed_agent()
# # agent.generate_stage_analyzer(verbose=True)
#
# print(welcome_agent())
# import re
#
# s = '("part1","part2")'
# pattern = r'\("([^"]*)","([^"]*)"\)'
#
# match = re.match(pattern, s)
#
# if match:
#     part1 = match.group(1)
#     part2 = match.group(2)
#     print("Part 1:", part1)
#     print("Part 2:", part2)
# else:
#     print("No match")




# file_path =r'C:\Users\Administrator\langchain_chatbot\product.txt'
# knowledge_base = build_knowledge_base(file_path)
# print(knowledge_base)
#
# answer = knowledge_base.invoke('上海三日游的产品价格是多少')
# print(answer)





# def check_content(pattern, text):
#     # 使用re.search检查字符串中是否存在匹配
#     if re.search(pattern, text):
#         return False
#     else:
#         return True
#
# pattern = r'\bquit\b'
#
# flag = True
# while flag:
#     agent.human_step()
#     agent.step()
#     history = agent.show_chat_history()
#     print(history)
#     agent.determine_conversation_stage()
#     flag = check_content(pattern,str(history[-2]))

#
# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# # 获取当前日期
# current_date = datetime.now()
#
# # 获取当前月份
#
# # 获取前7个月的月份
# seven_months_ago = current_date - relativedelta(month=7)
#
# print("当前月份:", current_date.strftime('%Y%m'))
# print("前7个月份:", seven_months_ago.strftime('%Y%m'))

# set_observation(db=1,key="9d15e7a0fa8c4ccf9124aada7d045740", queryRdmpFx="""{"admin":true,"authorities":[{"authority":"100020"},{"authority":"100000"},{"authority":"100001"},{"authority":"100100"}],"bossOrgId":"NX","browser":"Chrome 12","crossToken":"b8940fbfd40744f6bcedb7643b2d65e5","deptId":100,"email":"1**********@139.com","expireTime":1713959347584,"hasPerms":["system.notice.pub","busi.rwdtype.add.child","system.classmember.del","system.task.del","busi.orgrate.edit","system.user.auth","system.task.resume","system.role.auth","system.task.add","system.notice.del","datasource.import.delete","system.menu.edit","system.classmember.edit","datasource.import.import","system.rptAccAudit.audit","busi.orgrate.add","busi.rwdtype.add","system.role.add","system.task.edit","system.version.edit","system.assess.download","system.user.edit","system.file.upload","system.menu.del","system.file.delete","system.classmember.bind","system.assess.import","system.notice.edit","system.assess.auditFail","system.notice.add","system.user.show","busi.rwdtype.del","0","system.role.edit","system.version.add","system.business.audit","busi.orgrate.del","system.assess.submit","system.role.delete","system.assess.revocation","system.assess.modify","system.business.backToAdjust","datasource.import.export","system.version.del","system.rptAccAudit.reBackAudit","system.assess.upload","system.role.show","system.classmember.unbind","system.assess.auditSucc","datasource.import.edit","system.assess.export","busi.rwdtype.edit","monitor.sms.resend","system.user.delete","system.classmember.add"],"hasRole":["100020","100000","100001","100100"],"ipaddr":"127.0.0.1","isAdminAccount":"1","loginLocation":"内网IP","loginTime":1713952147584,"nickName":"孙宁","os":"Windows 10","password":"$2a$10$QNjJb8d3qsK.3ndw3TPSEeYv9J2uI9Vq27GjuDzJSB47n4zl4pLdS","phoneNumber":"158****5205","regionId":"0","regionName":"宁夏","sex":"1","token":"80b6cc7f-8e59-4dbc-862e-c79030a5496e","userId":59999981,"userLevel":"1","username":"孙宁"}""")
# print(get_observation(db=1,key="9d15e7a0fa8c4ccf9124aada7d045740"))
# print(get_observation(key="9d15e7a0fa8c4ccf9124aada7d045740"))

#
# class Http_Param(object):
#     # # 初始化
#     def __init__(self, URL ,APPID, APPKey):
#         self.URL = URL
#         self.APPID = APPID
#         self.APPKey = APPKey
#     # def __init__(self, URL):
#     #     self.URL = URL
#     # 生成url
#     def create_header(self):
#         appid = self.APPID
#         appKey = self.APPKey
#         uuid = getUUID()
#         # 24 + 32 + 8
#         appName = self.URL.split('/')[3]
#         for i in range(24 - len(appName)):
#             appName += "0"
#         capabilityname = appName
#         #print(len(capabilityname))
#         csid = appid + capabilityname + uuid
#         tmp_xServerParam = {
#         	"appid": appid,
#         	"csid": csid
#         }
#         xCurTime = str(math.floor(time.time()))
#         xServerParam = str(base64.b64encode(json.dumps(tmp_xServerParam).encode('utf-8')), encoding="utf8")
#         # turn to bytes
#         xCheckSum = hashlib.md5(bytes(appKey + xCurTime + xServerParam, encoding="utf8")).hexdigest()
#
#         header = {
#             "appKey": appKey,
#             "X-Server-Param": xServerParam,
#             "X-CurTime": xCurTime,
#             "X-CheckSum": xCheckSum,
#              "content-type": "application/json"
#         }
#         return header
# def getUUID():
#     return "".join(str(uuid.uuid4()).split("-"))
#
#
#     prompt = "You are ChatGLM3, a large language model trained by Zhipu.AI. Follow the user's"
#
#     # endpoint_url = "https://dsw-gateway-cn-shanghai.data.aliyun.com/dsw-321152/ide/proxy/8000/v1/chat/completions"
#     endpoint_url = "http://117.132.181.235:9050/nxmodelapi/v1/chat/completions"
#
#     httpParam = Http_Param(URL=base_url, APPID='chatbiid',
#                            APPKey='ee53663b8a16ce4a2c391bd4442debe6')
#
#     httpHeader = httpParam.create_header()
#
#     llm = ChatGLM3(
#         endpoint_url=endpoint_url,
#         max_tokens=4096,
#         # prefix_messages=messages,
#         top_p=0.9
#     )
#
#     # llm = Tongyi()
#     # llm_chain = LLMChain(prompt=prompt, llm=llm)
#     # response = llm_chain.invoke({"input": "你好"})
#     response = llm.invoke("你好")
#     print("===========" + response)

str_json = "{'nxcode': 'NX.01.01.02.001.14', 'token': '9d15e7a0fa8c4ccf9124aada7d045740', 'chat_history': '查询结算积分'}"
# str_json = json.loads(str_json.replace("'","\""))
# print(str_json, type(str_json))

data = json.loads(str_json.replace("'","\""))
# 确认 data 是一个列表
if not isinstance(data, list): # 输出：True
    raise ValueError("JSON must represent a list of elements")
# 访问列表中的元素
tuple_list = [(d["name"],d["value"]) for d in data]

print(tuple_list,type(tuple_list))