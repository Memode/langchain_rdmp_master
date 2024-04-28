import redis


def get_observation(key:str = "key1"):
    # 连接到本地Redis服务器，端口默认为6379
    redis_client = redis.StrictRedis(host='localhost', password="foobared", port=6379, db=0)
    # 读取数据
    observation = redis_client.get(key)
    # print(observation.decode('utf-8'))  # 解码字节串为字符串
    redis_client.delete('key1')
    # 关闭连接
    redis_client.close()
    if observation is None:
        observation = None
    else:
        observation = observation.decode('utf-8')
    return observation

def set_observation(key:str = "key1", queryRdmpFx:str = "queryRdmpFx"):
    # 连接到本地Redis服务器，端口默认为6379
    redis_client = redis.StrictRedis(host='localhost', password="foobared", port=6379, db=0)
    # 写入数据
    redis_client.set(key, queryRdmpFx)
    # 关闭连接
    redis_client.close()

