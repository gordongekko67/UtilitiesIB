#import redis
#client = redis.StrictRedis(host='demo-redis2.5og6vn.clustercfg.euc1.cache.amazonaws.com:6379', port=6379)
from redis import Redis
import logging

logging.basicConfig(level=logging.INFO)
redis = Redis(host='cloudredis.5og6vn.ng.0001.euc1.cache.amazonaws.com', port=6379, decode_responses=True, ssl=True)

if redis.ping():
    logging.info("Connected to Redis")
