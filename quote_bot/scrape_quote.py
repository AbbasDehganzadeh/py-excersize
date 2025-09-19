import json
import re

import requests
from bs4 import BeautifulSoup

count = 0
resp = requests.get(
    r"https://www.forbesindia.com/article/explainers/motivational-quotes/84853/1"
)
soup = BeautifulSoup(resp.text, "html.parser")

topics = soup.find(id="info").find_all("h2")
sections = soup.find(id="info").find_all("ol")

# TODO: give the topic base on text;
topic_re = re.compile(r"for [\w\s]+:")
sep_re = re.compile(r"[―—–-]+")
data = dict(topics=[{"uncategorized": [{"sumup": "uncategorized"}]}])
for topic, section in zip(topics, sections):
    indecesis = re.search(topic_re, topic.text)
    _, topic_summ = topic.text.split(":")
    if indecesis is not None:  # topic is unclear
        s = indecesis.span()
        if len(s) == 2:
            f, l = s[0], s[1]
        else:
            f, l = s, s
        raw_topic = topic.text[f + 4 : l - 1]  # remove unusechar
        dict_topic = {raw_topic: [{"summup": topic_summ}]}
        if not any([raw_topic in tmp.keys() for tmp in data["topics"]]):
            data["topics"].append(dict_topic)

    quotes_list = [tuple(re.split(sep_re, span.text)) for span in section]
    for q in quotes_list:
        if len(q) == 1:
            # print(count,"Item",q)
            # print("Len",len(q))
            continue
        count += 1

        joined = ",".join(q[0:-1])
        quote = joined.replace('"', "").strip().capitalize()
        person = " ".join([n.capitalize() for n in q[-1].split()])
        quote_dict = {"person": person, "quote": quote}
        if indecesis is None:
            data["topics"][0]["uncategorized"].append(quote_dict)
        else:
            topic = [tmp for tmp in data["topics"] if raw_topic in tmp.keys()]
            # print(topic)
            topic[0][raw_topic].append(quote_dict)

with open("quote.json", "w") as d:
    json.dump(data, d, indent=1, ensure_ascii=False)
print("{} quotes fetched!!".format(count))
