import json
import time

from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher


def publish_in_ws(image):
    data = dict()
    data["id"] = image.id
    converted = image.converted_datetime
    data["created"] = time.mktime(image.created.timetuple())
    data["converted_datetime"] = converted and time.mktime(converted.timetuple()) or None
    msg = RedisMessage(json.dumps(data))
    RedisPublisher(facility='foobar', broadcast=True).publish_message(msg)
