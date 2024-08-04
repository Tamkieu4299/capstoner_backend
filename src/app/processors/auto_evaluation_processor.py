import zipfile
from app.models.user_model import User
from app.models.question_model import Question
from app.models.assignment_model import Assignment
from app.crud.student_answer_crud import CRUDStudenAnswer
from app.crud.question_crud import CRUDQuestion
from app.crud.assignment_crud import CRUDAssignment
from app.models.student_answer_model import StudentAnswer
from ..utils import common, s3_driver
from openai import AzureOpenAI
from app.constants.config import Settings
import re
import os

settings = Settings()

sa_crud = CRUDStudenAnswer(StudentAnswer)
asm_crud = CRUDAssignment(Assignment)

question_crud = CRUDQuestion(Question)
llm = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION"),
)

initial_prompt = "I want you to act as an AI evaluating on students' coding work. I will provide you a text file of the coding question with points of the question in brackets (example: Question 1 (8pts)) and a text file of the standard marking criteria that you will need to follow to give recommended marks. I will provide you a folder contains coding works in text format and your task is to use artificial intelligence tools, such as natural language processing, to detect the programming language, give tailored feedback on how they can improve and write it in the Feedback section, only give 1 total recommended marks of the question point in the Score section, separated by a break line. Only use the marking criteria for standardizing the mark, do not give mark completely based on the provided marking criteria. You will also be given a sample marking from real instructors for each question in an Excel file, please also use this Excel file to give out the best recommended mark and tailored feedback for students. Here are the marking criteria, test question and the students' work in text:"

def extract_score(text):
    pattern = r'\d+/\d+'
    match = re.search(pattern, text)
    if match:
        return match.group()
    return None

async def get_content_after_question_title(text):
    pattern = r"(Question \d+ \(\d+ pts\))"

    parts = re.split(pattern, text)

    result = []

    for i in range(1, len(parts), 2):
        question_content = parts[i + 1].strip()
        result.append(question_content)
    return result


async def bulk_create_result(ids, result, db):
    res = await get_content_after_question_title(result)
    payload = []

    for i in range(len(ids)):
        score = extract_score(res[i])
        item = {"id": ids[i], "result": res[i], "score": score}
        print(item)
        payload.append(item)

    sa_crud.bulk_update(payload, db)


async def auto_evaluation_processor(asm_id):
    sessionmaker = settings.psql_factory.create_sessionmaker()
    with sessionmaker() as db:
        asm = asm_crud.read(asm_id, db)
        marking_criteria = s3_driver.get_file(asm.marking_criteria_filepath)
        question_content = s3_driver.get_file(asm.questions_filepath)

        sas = sa_crud.read_by_assignment_id_sort_by_student_name(asm_id, db)
        current_student_name = None
        processed = ""
        accumulate_ids = []
        for ind, sa in enumerate(sas):
            if (
                current_student_name
                and sa.student_name != current_student_name
            ) or ind == len(sas) - 1:
                
                if ind == len(sas) - 1:
                    accumulate_ids.append(sa.id)
                    processed += sa.protected_answer + "\n"

                prompt = " ".join(
                    [
                        initial_prompt,
                        "\nHere's the marking criteria:\n" + marking_criteria,
                        "\nHere's the questions:\n" + question_content,
                        "\nHere's the studentent answer:\n" + processed,
                    ]
                )
                messages = [
                    {
                        "role": "system",
                        "content": "You are a teacher assistant who help to evaluate and give mark student code assesment based on the marking criteria.",
                    },
                    {"role": "user", "content": prompt},
                ]
                try:
                    # completion = llm.chat.completions.create(
                    #     model="AzureCodeGrader",
                    #     messages=messages,
                    #     temperature=0.7,
                    #     max_tokens=800,
                    #     top_p=0.95,
                    #     frequency_penalty=0,
                    #     presence_penalty=0,
                    #     stop=None,
                    # )
                    dummy = """Question 1 (8 pts)
Score: 7/8
Feedback:
- The program correctly prompts the user to enter three float numbers.
- The program correctly checks if a number is the sum of the other two numbers.
- The program correctly prints the result as "YES" or "NO".
- However, there is a missing blank line between the code sections, which does not follow the code style requirement.
Overall, the program is correct and efficient, but there is a minor issue with code style.
Question 2 (8 pts)
Score: 6/8
Feedback:
- The program correctly prompts the user to enter an even integer.
- The program correctly calculates and prints the sum of all even values from 0 to the input number.
- The program correctly stops when the user inputs an odd integer and prints an error message.
- However, there is a missing blank line between the code sections, which does not follow the code style requirement.
- The program does not have descriptive comments for each code section, which does not follow the code style requirement.
Overall, the program is correct and efficient in terms of functionality, but there are issues with code style.
Question 3 (9 pts)
Score: 7/9
Feedback:
- The program correctly prompts the user to enter an integer between 1 and 10 inclusively.
- The program correctly displays the pattern based on the input number.
- However, there is a missing blank line between the code sections, which does not follow the code style requirement.
- The program does not have descriptive comments for each code section, which does not follow the code style requirement.
Overall, the program is correct and efficient in terms of functionality, but there are issues with code style.
Total Score: 20/25"""
                    await bulk_create_result(
                        accumulate_ids,
                        dummy,
                        # completion.choices[0].message.content,
                        db,
                    )
                except Exception as err:
                    print(err)
                accumulate_ids = []
                processed = ""

            current_student_name = sa.student_name
            accumulate_ids.append(sa.id)
            processed += sa.protected_answer + "\n"
    asm_crud.update(asm_id, {"evaluation_status": True}, db)

"""

import os
import requests
import base64

# Configuration
GPT4V_KEY = "YOUR_API_KEY"
IMAGE_PATH = "YOUR_IMAGE_PATH"
encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
headers = {
    "Content-Type": "application/json",
    "api-key": GPT4V_KEY,
}

# Payload for the request
payload = {
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are an AI assistant that helps people find information."
        }
      ]
    }
  ],
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 4096
}

GPT4V_ENDPOINT = "https://fine-tune-testing.openai.azure.com/openai/deployments/finetunetest/chat/completions?api-version=2024-02-15-preview"

# Send request
try:
    response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
except requests.RequestException as e:
    raise SystemExit(f"Failed to make the request. Error: {e}")

# Handle the response as needed (e.g., print or process)
print(response.json())

"""
