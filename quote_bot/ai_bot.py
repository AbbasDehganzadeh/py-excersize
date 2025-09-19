import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
  base_url=os.getenv("OPENAI_API_URL"),
  api_key=os.getenv("OPENAI_API_KEY"),
)
MODEL="deepseek/deepseek-chat-v3-0324:free"

Template = """I'll give you a word and you follow these steps:

1. pick one of these category, base on word (inspirational, work, travel, life, love, freedom, death, general)
2. select a quote that feeds into that category, related to the word
3. translate person, and quote to farsi
4. format the quote like the following:
category: [category]
[PERSON] says:
"[QUOTE]"
[PERSON] میگه:
"[QUOTE]"
5 just show the output in specified format, nothing else.
"""


def getBotQuote(word):
	completion = client.chat.completions.create(
	  model="deepseek/deepseek-r1-0528:free",
	  messages=[
		{"role": "system", "content": Template},
		{"role": "user", "content": "word: `{0}` ".format(word)},
	  ]
	)
	response = completion.choices[0].message.content
	response = cleanBotResponse(response)
	return response


def cleanBotResponse(text):
    return text.lower()

