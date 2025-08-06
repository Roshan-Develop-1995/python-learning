# import requests
# from bs4 import BeautifulSoup
# from IPython.display import Markdown,display

# OLLAMA_API = "http://localhost:11434/api/chat"
# HEADERS = {"Content-Type": "application/json"}
# MODEL = "llama3.2"
#
# messages=[
#     {"role": "user", "content": "Describe some of the business applications of Generative AI"}
# ]
#
# payload = {
#     "model": MODEL,
#     "messages" : messages,
#     "stream" : False
# }
#
# response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
# print(response.json()['message']['content'])
#


import ollama
import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown,display
from langchain_experimental.graph_transformers.llm import system_prompt

MODEL = "llama3.2"
# messages=[
#     {"role": "user", "content": "Describe some of the business applications of Generative AI"}
# ]
# response = ollama.chat(model=MODEL, messages=messages)
# print(response['message']['content'])

# website summarizer for local ollama

# Some websites need you to use proper headers when fetching them:
WEBPAGE_HEADERS = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=WEBPAGE_HEADERS)
        bs = BeautifulSoup(response.content, 'html.parser')
        self.title = bs.title.string if bs.title else "No title found"
        for irrelevant in bs.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = bs.body.get_text(separator="\n", strip=True)

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

def summarize(url):
    website = Website(url)
    response = ollama.chat(model=MODEL, messages=messages_for(website))
    return response['message']['content']

def display_summary(url):
    summary = summarize(url)
    print(summary)

#Execute
display_summary("https://edwarddonner.com")