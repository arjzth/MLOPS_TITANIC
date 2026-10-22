import json
import redis


class RedisFeatureStore:
    def __init__(self , host="localhost" , port = 6379 , db=0):
        self.client = redis.StrictRedis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )

    def store_features(self,entity_id,features):
        key = f"entity:{entity_id}:features"
        self.client.set(key , json.dumps(features))

    def get_features(self,entity_id):
        key = f"entity:{entity_id}:features"
        features = self.client.get(key)
        if features:
            return json.loads(features)
        return None

    def store_batch_features(self,batch_data):
        for entity_id , features in batch_data.items():
            self.store_features(entity_id,features)