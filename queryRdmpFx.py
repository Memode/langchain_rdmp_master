import json

import pymysql
import re



def queryRdmp(channel_name, channel_code):
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

    sql = f"select * from test_db.reward_fx where A010 like '%{channel_name}%' or A011 like '%{channel_code}' order by 统计月份 limit 6"
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
    print(queryRdmp("燕鸽湖手机专卖店"))
