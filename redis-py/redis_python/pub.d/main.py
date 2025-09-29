import json
import logging
import os
import random
import re

from itertools import takewhile
import dotenv
import lxml.etree
import requests
import redis
from redis_python.helper import format_pack, str_join, wait


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


def publish(r, pack):
    ''' publush packages
        convert packages to json-string
        sends data to broker
        if it succed logs output
        if not, retries.
    '''
    try:
        log.debug("PACK: {}".format(pack))
        data = json.dumps(pack, ensure_ascii=False).encode("utf8")
        rcvd = r.publish(CHANNEL, data)
        if rcvd:
            package = format_pack(data)
            print("{} was sent!".format(package))
    except redis.ConnectionError as e:
        log.error("PUBSUBERR:", e)
        log.error("\tWill attempt to retry")
    except:
        err = "FATAL: Something went wrong when publishing!"
        log.critical(err)
        raise ConnectionError(err)
    return rcvd


def make_pack(mod):
    ''' make & prepare package
        - request to web
        - choose one at random
        - clip it to modules
    '''
    url = f"https://emojidb.org/{mod['label']}-emojis"
    log.debug("request to {}...".format(url))
    try:
        html = requests.get(url)
        html.raise_for_status()
    except:
        err = "FATAL: Something went wrong when preparing!"
        log.critical(err)
        raise ConnectionError(err)

    parser = lxml.etree.HTMLParser(encoding="utf-8")
    ## extract elemets
    root = lxml.etree.fromstring(html.content, parser)
    elems = root.xpath(r'//*[@class="emoji"]')
    n_elem = list(takewhile(lambda x: len(x.text) == 1, elems))[:10]
    log.info("{} modules found!".format(len(n_elem)))
    log.debug(" {} ".format([elem.text for elem in n_elem]))
    ## chosse element
    if len(n_elem) == 0:
        mod["unit"] = 0
        mod["module"] = ''
        return mod
    elem = random.choice(n_elem)
    mod["module"] = elem.text
    tx = f'\tUNIT: {mod["unit"]} MODULE: {mod["module"]}'
    if log.isEnabledFor(logging.INFO):
        log.info(tx)
    log.debug(tx + f' LABEL: {mod["label"]}')
    return mod


def proc_input(text):
    ''' process input
        validate input into defined format,
        and make modules var
    '''
    texts = text.split(",")
    mod_re = re.compile(r"[^\W_]\w*")
    text_re = re.compile(r"^(?P<unit>\d+)\s(?P<label>{})$".format(mod_re.pattern))
    log.debug("using pattern `{}` for validation:".format(text_re))
    modules = list(dict())
    for text in texts:
        log.debug("validate text `{}`".format(text))
        match_txt = text_re.match(text.strip())
        if match_txt:
            module = match_txt.groupdict()
            module["unit"] = int(module["unit"])
            modules.append(module)
        else:
            err = str_join(
                ("The input is wrong,"),
                ("cannot process;\n"),
                ("please write with following format:\t"),
                (" [UNIT] [MODULE], [NUM] [1_WORLD]"),
            )
            log.error(err)
            raise ValueError(err)
    return modules


rdb = redis.Redis(host=REDIS_HOST)


def main():
    while True:
        inp = input("{}> ".format(CHANNEL))
        log.debug("start processing input...\n{}".format(inp))
        mods = proc_input(inp) # validations
        log.debug("supply packages...\n{}".format([mod.items() for mod in mods]))
        # in every packages contains three modules, at most
        lm = len(mods)
        div = lm // 3 if lm % 3 == 0 else lm // 3 + 1
        pkg = [[] for _ in range(div)]
        idx, thres = 0, 3
        for mod in mods:
            if len(pkg[idx]) == thres:
                log.debug("wrap package...\n{}".format(pkg[idx]))
                wait(1, 3, 2)
                idx += 1
            pkg[idx].append(make_pack(mod))
            wait(0.5, 1, 2)
        for pack in pkg:
            log.debug("start publishing packages...")
            rcvd = 0
            while not rcvd:
                rcvd = publish(rdb, pack)
                wait(1, 5, 0)
            wait(3, 5)
        log.debug(" start over...")


if __name__ == "__main__":
    log.info("Start providing...")
    try:
        main()
    except KeyboardInterrupt:
        pass
