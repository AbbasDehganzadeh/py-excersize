import logging
import os
import time

import dotenv
import redis
from redis_python.helper import format_pack, wait


### constants
dotenv.load_dotenv("../.env")
LOG_LEVEL = os.getenv("LOG_LEVEL", default="INFO")
LOG_FILE = os.getenv("LOG_FILE", default="")
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
CHANNEL = os.getenv("CHANNEL")
if not CHANNEL:
    log.error("`CHANNEL` not speicified, please provide in .env file")


### logging
logging.basicConfig(
    filename=LOG_FILE,
    format="[%(asctime)s] %(name)s : %(message)s",
    level=LOG_LEVEL,
)
log = logging.getLogger(__name__)


def subscribe(r):
    e = r.pubsub()

    e.subscribe(CHANNEL)
    while True:
        try:
            message = e.get_message()
        except redis.ConnectionError as e:
            log.error("PUBSUBERR:", e)
            log.error("\tWill attempt to retry")
            wait(5, 10, 0)
        except:
            err = "FATAL: Something went wrong when subscribing!"
            log.critical(err)
            raise ConnectionError(err)

        data = message and message.get("data")
        if type(data) is bytes:
            package = format_pack(data)
            print("{} is recieved!".format(package))
        elif type(data) is int:
            print("{}> ".format(CHANNEL), end='')
            log.debug("Provider recognized...")
        else:
            log.info("Listening state...")
        wait(3, 6)


rdb = redis.Redis(host=REDIS_HOST)

if __name__ == "__main__":
    log.info("Start listening...")
    try:
        subscribe(rdb)
    except KeyboardInterrupt:
        pass
