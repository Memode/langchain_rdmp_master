import redis


def get_user_info(host:str ="localhost", password:str = "foobared", port:int =6379, db: int = 1, key:str = "key1"):
    # 连接到本地Redis服务器，端口默认为6379
    redis_client = redis.StrictRedis(host=host, password=password, port=port, db=db)
    # 读取数据
    user_info = redis_client.get(key)
    # print(observation.decode('utf-8'))  # 解码字节串为字符串
    # 关闭连接
    redis_client.close()
    if user_info is None:
        user_info = None
    else:
        user_info = user_info.decode('utf-8')
    return user_info


def get_observation(host:str ="localhost", password:str = "foobared", port:int =6379, db: int = 0, key:str = "key1"):
    # 连接到本地Redis服务器，端口默认为6379
    redis_client = redis.StrictRedis(host=host, password=password, port=port, db=db)
    # 读取数据
    observation = redis_client.get(key)
    # print(observation.decode('utf-8'))  # 解码字节串为字符串
    redis_client.delete(key)
    # 关闭连接
    redis_client.close()
    if observation is None:
        observation = None
    else:
        observation = observation.decode('utf-8')
    return observation


def set_observation(host:str ="localhost", password:str = "foobared", port:int =6379, db: int = 0, key:str = "key1", queryRdmpFx:str = ""):
    # 连接到本地Redis服务器，端口默认为6379
    redis_client = redis.StrictRedis(host=host, password=password, port=port, db=db)
    # 写入数据
    redis_client.set(key, queryRdmpFx)
    # 关闭连接
    redis_client.close()

