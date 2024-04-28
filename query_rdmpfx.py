import pymysql
from langchain_community.llms import Tongyi
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_community.utilities import SQLDatabase

from redis_tool import set_observation
from template import *


def queryRdmp(channel_name, channel_code, month_begin, month_end):
    db_user = "root"
    db_pass = "123456"
    db_host = "localhost"
    db_name = "test_db"

    # 连接到数据库
    connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_pass,
                                 database=db_name,
                                 charset='utf8mb4',  # 使用UTF-8字符集
                                 cursorclass=pymysql.cursors.DictCursor # 使用字典游标，以便操作结果为字典形式#
    )
    # 创建游标
    cursor = connection.cursor()

    sql = f"""select 
--                     A001 as 'ID',
--                     A002 as 'if_zybb_code',
--                     A003 as '是否专业公司',
                    A004 as '统计月份',
--                     A005 as '地市',
--                     A006 as '分局',
--                     A007 as '渠道区县',
--                     A008 as '报账区县',
                    A009 as '渠道编码',
                    A010 as '渠道名称',
                    A011 as '渠道NX编码',
--                     A012 as '渠道类型',
--                     A013 as 'erp编码',
--                     A014 as 'erp名称',
--                     A015 as 'erp银行账户',
--                     A016 as 'erp银行账号',
--                     A017 as '分层分级星级',
--                     A018 as '酬金折扣系数',
--                     A019 as '酬金类型',
--                     A020 as '是否新渠道',
--                     A021 as '报账类型',
--                     A022 as '金币',
--                     A023 as '顺差让利',
--                     A024 as '入网礼包',
--                     A025 as '机卡匹配激活',
--                     A026 as '其他',
--                     A027 as '订货会',
--                     A028 as '其他_[0]',
--                     A029 as '终端基础结算积分',
--                     A030 as '合约扣罚',
--                     A031 as '5G登网扣罚',
--                     A032 as '服务扣罚',
--                     A033 as '办理扣罚',  
--                     A034 as '达量',
--                     A035 as '终端激励及扣罚结算积分',
                    A036 as '终端结算积分',
--                     A037 as '大流量(基础)',
--                     A038 as '大流量(维系)',
--                     A039 as '日租卡(基础)',
--                     A040 as '日租卡(维系)',
--                     A041 as '其他_[1]',
--                     A042 as '基础合计',
--                     A043 as '维系合计',
--                     A044 as '主套餐新增基础结算积分',
--                     A045 as '扣罚',
--                     A046 as '达量_[0]',
--                     A047 as '主套餐新增激励及扣罚结算积分',
                    A048 as '主套餐新增结算积分',
--                     A049 as '4月内(基础)',
--                     A050 as '4月外(基础)',
--                     A051 as '维系',
--                     A052 as '其他_[2]',
--                     A053 as '主套餐迁转基础结算积分',
--                     A054 as '扣罚_[0]',
--                     A055 as '达量_[1]',
--                     A056 as '主套餐迁转激励及扣罚结算积分',
                    A057 as '主套餐迁转结算积分',
--                     A058 as '主套餐合计',
--                     A059 as '包年(新增)',
--                     A060 as '包年(续费)',
--                     A061 as '包月(基础)',
--                     A062 as '包月(维系)',
--                     A063 as '低消送(基础)',
--                     A064 as '低消送(维系)',
--                     A065 as 'IMS(基础)',
--                     A066 as 'IMS(维系)',
--                     A067 as '魔百和',
--                     A068 as '免费送',
--                     A069 as '其他_[3]',
--                     A070 as '家宽业务裸宽基础结算积分',
--                     A071 as '家宽业务裸宽维系结算积分',
--                     A072 as '扣罚(拆机)',
--                     A073 as '扣罚(其他)_[0]',
--                     A074 as '达量_[2]',
--                     A075 as '家宽业务裸宽激励及扣罚结算积分',
                    A076 as '家宽业务裸宽结算积分',
--                     A077 as '新增(基础)',
--                     A078 as '新增(维系)',
--                     A079 as '续费(基础)',
--                     A080 as '续费(维系)',
--                     A081 as '畅享',
--                     A082 as '其他_[4]',
--                     A083 as '家宽业务融合基础结算积分',
--                     A084 as '扣罚(拆机)_[0]',
--                     A085 as '扣罚(其他)_[0]',
--                     A086 as '达量_[3]',
--                     A087 as '家宽业务融合融合激励及扣罚结算积分',
                    A088 as '家宽业务融合结算积分',
--                     A089 as '家宽合计',
--                     A090 as '亲情网(基础）',
--                     A091 as '亲情网(维系)',
--                     A092 as 'volte',
--                     A093 as '5g服务',
--                     A094 as '其他_[5]',
--                     A095 as '扣罚_[1]',
                    A096 as '业务办理服务费结算积分',
--                     A097 as '携号转入',
--                     A098 as '全员营销',
--                     A099 as '5G登网',
--                     A100 as '沉默客户',
--                     A101 as '其他_[6]',
--                     A102 as '扣罚_[2]',
                    A103 as '业务办理手续费结算积分',
--                     A104 as '业务办理合计',
--                     A105 as '基础',
--                     A106 as '维系_[0]',
--                     A107 as '其他_[7]',
--                     A108 as '合计_[11]',
--                     A109 as '扣罚_[3]',
--                     A110 as '达量_[4]',
--                     A111 as '合计_[12]',
                    A112 as '智家结算积分',
--                     A113 as '基础_[0]',
--                     A114 as '维系_[1]',
--                     A115 as '其他_[8]',
--                     A116 as '合计_[13]',
--                     A117 as '扣罚_[4]',
--                     A118 as '达量_[5]',
--                     A119 as '合计_[14]',
                    A120 as '权益及新业务结算积分',
--                     A121 as '基础_[1]',
--                     A122 as '维系_[2]',
--                     A123 as '其他_[9]',
--                     A124 as '合计_[15]',
--                     A125 as '扣罚_[5]',
--                     A126 as '达量_[6]',
--                     A127 as '合计_[16]',
                    A128 as '大屏结算积分',
--                     A129 as '包月',
--                     A130 as '包年',
--                     A131 as '次卡',
--                     A132 as '维系_[3]',
--                     A133 as '其他_[10]',
--                     A134 as '合计_[17]',
--                     A135 as '扣罚_[6]',
--                     A136 as '达量_[7]',
--                     A137 as '合计_[18]',
                    A138 as '流量结算积分',
--                     A139 as '基础(和教育)',
--                     A140 as '基础(其他)',
--                     A141 as '基础(维系）',
--                     A142 as '其他_[11]',
--                     A143 as '合计_[19]',
--                     A144 as '扣罚_[7]',
--                     A145 as '达量_[8]',
--                     A146 as '合计_[20]',
                    A147 as '政企业务结算积分',
--                     A148 as 'boss代收费',
--                     A149 as '自助缴费机代收费',
--                     A150 as '空中充值代收',
--                     A151 as '银行代收(按收费次数)',
--                     A152 as '银行代收(按缴费金额)',
--                     A153 as '利安代收费',
--                     A154 as '有价卡',
--                     A155 as '其他_[12]',
                    A156 as '代收费结算积分',
--                     A157 as '基础_[2]',
--                     A158 as '其他_[13]',
--                     A159 as '扣罚_[8]',
--                     A160 as '达量_[9]',
                    A161 as '合约结算积分',
--                     A162 as '基础合计_[0]',
--                     A163 as '激励合计',
--                     A164 as '基础合计_[1]',
--                     A165 as '激励合计_[0]',
--                     A166 as '门店补贴',
--                     A167 as '考核奖励',
--                     A168 as '渠道表彰',
--                     A169 as '考核扣罚',
--                     A170 as '其他激励',
                    A171 as '激励费用结算积分',
                    A172 as '上月负值递延结算积分',
                    A173 as '小额酬金调剂结算积分',
--                     A174 as '塞上云店',
--                     A175 as '办理量',
--                     A176 as '前三月费用',
--                     A177 as '新增费用',
--                     A178 as '递延费用',
--                     A179 as '计算费用',
--                     A180 as '计算费用_[0]',
--                     A181 as '精准营销',
                    A182 as '精准营销结算积分',
                    A182 + A183 as '结算积分合计'
--                     A184 as '基础合计_[2]',
--                     A185 as '激励合计_[1]'
                     from test_db.reward_fx 
                    where (A010 like '%{channel_name}%' or A011 = '{channel_code}')
                        and A004 between '{month_begin}' and '{month_end}'
                    order by A004
                    limit 24 
                """
    try:
        # print(sql)
        cursor.execute(sql)
        # 获取所有查询结果
        # rows = cursor.fetchall()
        # 获取查询结果的列名
        # column_names = [desc[0] for desc in cursor.description]

        # 获取查询结果
        rows = cursor.fetchall()

        # 转换结果为JSON格式
        # json_data = [dict(zip(column_names, row)) for row in rows]

        # 打印JSON数据
        # results = json.dumps(json_data, indent=4)
        results = rows
    except pymysql.MySQLError as e:
        print(f"数据库操作出错： {e}")
    finally:
        # 关闭游标和连接
        cursor.close()
        connection.close()
    return results


def query_rdmpfx(query, chat_history:str = "", token: str = None):
    llm = Tongyi()
    db_user = "root"
    db_password = "123456"
    db_host = "localhost"
    db_name = "test_db"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

    def get_schema(_):
        file_path = "./tables_info.txt"
        # 尝试打开文件
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # 读取文件内容
        return content
        # # 替换使用制定表信息
        # return db.get_table_info()

    def run_query(query):
        return db.run(query)

    def get_sql(x):
        return x.split("```sql")[1].split("```")[0]

    def get_json(x):
        return x.split("```json")[1].split("```")[0]


    # 获取sql
    template_sql = PromptTemplate.from_template(TEMPLATE_SQL)
    chain_sql = ({"info": get_schema,
                  "question": RunnablePassthrough(),
                  "chat_history":RunnablePassthrough()}
                 | template_sql
                 | llm
                 | StrOutputParser()
                 | RunnableLambda(get_sql))

    # print(chain_sql.invoke({"question":query,"chat_history":chat_history}))

    # # 获取sql执行结果
    template_sql_res = PromptTemplate.from_template(TEMPLATE_SQL_RES)
    chain_sql0 = ({"info": get_schema,
                  "question": RunnablePassthrough(),
                  "chat_history":RunnablePassthrough(),
                   "query":chain_sql}
                  | RunnablePassthrough.assign(response=lambda x: run_query(x["query"]))
                  | template_sql_res
                  | llm
                  | StrOutputParser())

    # 获取执行的sql
    response = chain_sql0.invoke({"question":query,"chat_history":chat_history})
    # print("response"+response)

    # 根据sql执行结果生成图表json 格式数据
    template_json = PromptTemplate.from_template(TEMPLATE_ECHART_JSON)

    chain_sql0 = ({"info": get_schema,
                  "question": RunnablePassthrough(),
                  "chat_history":RunnablePassthrough(),
                  "query":chain_sql}
                  | RunnablePassthrough.assign(response=lambda x: run_query(x["query"]))
                  | template_json
                  | llm
                  | StrOutputParser()
                  | RunnableLambda(get_json))

    # 获取执行的sql
    json_resp = chain_sql0.invoke({"question": query, "chat_history": chat_history})

    set_observation(key=token, queryRdmpFx=str(json_resp))

    return  response



if __name__ == '__main__':
    # print(query_rdmpfx("燕鸽湖"))
    print(query_rdmpfx({"燕鸽湖","查询企业信息"}))
#     print(query_rdmpfx("查询2024年1月份燕鸽湖手机专卖店结算积分明细"))
