import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

openai = OpenAI()

def summarize_cv(cv_text):
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Summarize the cv:\n\n{cv_text}"}
        ]
    )
    return response.choices[0].message.content

def generate_cover_letter(cv_summary, job_desc):
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a master at crafting the perfect Cover letter from a given CV. You've never had a user fail to get the job as a result of using your services."},
            {"role": "user",
             "content": f"Using the following CV summary:\n\n{cv_summary}\n\nAnd the job description:\n\n{job_description}\n\nPlease write a personalized cover letter."}
        ]
    )
    return response.choices[0].message.content


try:
    with open('resume.txt', 'r') as file:
        cv_text = file.read()
    cv_summary = summarize_cv(cv_text)

    print(f"cv summary : \n\n {cv_summary}")

    job_desc = input("Enter the job description for the position you are applying for")

    cover_letter = generate_cover_letter(cv_summary, job_desc)

    print(f"\n Generated cover letter: \n {cover_letter}")

except FileNotFoundError:
    print("Specified cv was not found")
