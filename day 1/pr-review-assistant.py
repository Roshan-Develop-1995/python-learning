import os
import requests
from dotenv import load_dotenv
from IPython.display import Markdown, display
from openai import OpenAI, api_key

load_dotenv(override=True)
api_key = os.getenv('')
github_token = os.getenv('')
openai = OpenAI()

def extract_diff_from_pr(pr_url: str) -> str:
    parts = pr_url.rstrip("/").split("/")
    owner, repo, pr_number = parts[3], parts[4], parts[6]

    api_url = f"https://github.com/{owner}/{repo}/pull/{pr_number}.diff"
    headers = {
        "Accept": "application/vnd.github.v3.diff",
        "Authorization" : f"token {github_token}"
    }

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    return response.text

system_prompt = """You are an assistant that reviews code and provides concise, constructive feedback based on best practices. 
Focus on readability, architecture, performance, security, testability, and adherence to style guides.
Highlight issues and suggest improvements clearly. Respond in English and in markdown."""

def user_prompt_for(code_diffs):
    user_prompt = "You are reviewing the following code diffs"
    user_prompt += ". Please provide a concise code review focused on best practices: readability, architecture, performance, security, testability, and style guide adherence.\n"
    user_prompt += "Use a numbered list and be constructive. Suggest improvements where necessary, and highlight what was done well.\n\n"
    user_prompt += code_diffs
    return user_prompt

def code_review_for(code_diffs):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(code_diffs)}
    ]

def review_pr_from(pr_link):
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = code_review_for(extract_diff_from_pr(pr_link))
    )
    return response.choices[0].message.content

def display_code_review(pr_link):
    code_review = review_pr_from(pr_link)
    display(Markdown(code_review))

display_code_review("")