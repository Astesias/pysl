import redis

# 创建 Redis 连接
r = redis.Redis(host='localhost', port=6379, db=0)

# 定义要保存的字典
data = {'key1': 'value1', 'key2': 'value2'}

# 将字典保存到 Redis 哈希中
for key, value in data.items():
    r.hset('my_hash', key, value)

# 从 Redis 中获取保存的字典
result = r.hgetall('my_hash')

# 将结果转为 Python 字典
data = {key.decode(): value.decode() for key, value in result.items()}
print(data)
