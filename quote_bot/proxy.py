import json
import os

from lxml import etree
import lxml.etree
import requests

from telebot.util import CustomRequestResponse


def custom_proxy(method, url, **kwargs):
    """The custom proxy via telegram
    It sends request from third-party website, and parses the results.
    """

    full_url = url
    query = "?"
    if kwargs.get("params", None) is not None:
        for param, value in kwargs["params"].items():
            query += "{}={}&".format(param, value)
        full_url += query[:-1]
    print(full_url)

    payload = {
        "UrlBox": full_url,
        "AgentList": "Opera",
        "MethodList": method.upper(),
    }

    html = requests.post(os.getenv("PROXY_URL"), payload)

    parser = etree.HTMLParser(encoding="utf-8")
    root = etree.fromstring(html.content, parser)
    elem = root.xpath(r'//*[@id="ResultData"]/pre')

    with open("index.html", "w") as f:  # It saves the parsed output
        f.writelines(f"f {full_url}\m")
        f.writelines("-" * 100 + "\n\n")
        f.writelines(str(elem))
        f.write(elem[0].text)

    # It makes a payload into proper response
    data = CustomRequestResponse(elem[0].text)
    # data = json.loads(elem[0].text)

    return data
