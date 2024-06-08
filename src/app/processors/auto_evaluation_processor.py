import zipfile
from app.models.user_model import User
from app.models.question_model import Question
from  app.models.assignment_model import Assignment
from app.crud.student_answer_crud import CRUDStudenAnswer
from app.crud.question_crud import CRUDQuestion
from app.models.student_answer_model import StudentAnswer
from ..utils import common
from openai import AzureOpenAI
from app.constants.config import Settings

settings = Settings()

sa_crud = CRUDStudenAnswer(StudentAnswer)
question_crud = CRUDQuestion(Question)
llm = AzureOpenAI(
    azure_endpoint=settings.AZURE_ENDPOINT,
    api_key=settings.AZURE_API_KEY,
    api_version=settings.AZURE_API_VERSION,
)

initial_prompt = "You are a teacher assistant who helps to grade student code assessment."

async def auto_evaluation_processor(student_answer_data, zip_file):
    sessionmaker = settings.psql_factory.create_sessionmaker()
    with sessionmaker() as db:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                with zip_ref.open(file_name) as extracted_file:
                    student_name, question_number = common.extract_student_info(file_name)
                    q = question_crud.read_by_title(student_answer_data.assignment_id, question_number, db)
                    if not q:
                        print("found no question") 
                        continue
                    file_data = extracted_file.read()
                    student_answer = file_data.decode('utf-8')
                    prompt = " ".join(
                        [initial_prompt, q.instruction, student_answer, q.marking_criteria]
                    )
                    messages = [
                        {
                            "role": "system",
                            "content": "You are a teacher assistant who help to grade student code assesment.",
                        },
                        {"role": "user", "content": prompt},
                    ]
                    completion = llm.chat.completions.create(
                        model="AzureCodeGrader",
                        messages=messages,
                        temperature=0.7,
                        max_tokens=800,
                        top_p=0.95,
                        frequency_penalty=0,
                        presence_penalty=0,
                        stop=None, 
                    )
                    sa_dict = student_answer_data.__dict__
                    sa_dict["result"] = completion.choices[0].message.content
                    sa_dict["answer"] = student_answer
                    sa_dict["student_name"] = student_name
                    sa_dict["question_id"] = q.id
                    sa_dict["question_title"] = q.question_title
                    await sa_crud.create(sa_dict, db)