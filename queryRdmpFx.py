import json

import pymysql
import re



def queryRdmp(channel):
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
    # 使用正则表达式截取字母和数字
    pattern = r'NX.[a-zA-Z.0-9]+'
    match = re.findall(pattern, channel)


    channelCode = match[0]
    channelName = channel.replace(channelCode,'')

    sql = f"select * from tmp_fx_240415 where 渠道名称 like '%{channelName}%' or 渠道NX编码 like '%{channelCode}' order by 统计月份 limit 5"
    try:
        print(sql)
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

if __name__ == '__main__':
    print(queryRdmp("燕鸽湖手机专卖店NX.01.01.02.001.14"))