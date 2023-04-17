from rediscluster import RedisCluster

startup_nodes = [{"host": "demo-redis.5og6vn.ng.0001.euc1.cache.amazonaws.com", "port": "6379"}]

# Note: decode_responses must be set to True when used with python3
rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

rc.set("foo", "bar")

print(rc.get("foo"))