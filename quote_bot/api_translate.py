import json
import re
import requests

BASE_URL = "http://localhost:8100/translate"


def clean_author(text):
    """It removes abbrivations from person"""
    author_chunk = re.split(r"\s\w\.", text)
    return "".join(author_chunk)


def translate(source):
    """It gets a source`text`, and returns a translated text"""
    body = {"text": source, "to": "fa"}
    resp = requests.post(BASE_URL, json=body)
    data = json.loads(resp.text)["translatedText"]
    return data
