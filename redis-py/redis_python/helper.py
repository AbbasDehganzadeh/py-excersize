import json
import logging
import random
import time


log = logging.getLogger(__name__)


class Token:
    PACK_PL = "packages"
    PACK_SG = "package"
    COMMA = ","
    AND = "and"


def format_pack(data):
    """ format package
        it converts from json-bytes to dict-
        it provides standard format for logging pack.
    """
    log.debug("formatting...")
    pack = json.loads(data.decode())
    part = []
    for idx, pkg in enumerate(pack):
        if pkg["unit"] == 0:  # nothing!
            continue
        log.debug("\t {}".format(data))
        if idx != 0:
            part.append(Token.COMMA)
            if idx + 1 == len(pack):
                part.append(Token.AND)
        elif pkg["unit"] == 1 or pkg["unit"] == 2:
            part.extend([Token.PACK_SG, pkg["module"] * int(pkg["unit"])])
        else:  # more than two,
            part.extend([str(pkg["unit"]), Token.PACK_PL, pkg["module"]])

    texts = str_join(part)
    return texts.capitalize()


def str_join(txts):
    """ joins an iteration of strings """
    return " ".join(txts)


def wait(low=0, high=1, dec=1):
    ''' waits in custom mode:
        low <= high: dec >= 0
    '''
    num = round(random.uniform(low, high), dec)
    log.debug("Waiting {}s".format(num))
    time.sleep(num)

