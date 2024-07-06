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

settings = Settings()

sa_crud = CRUDStudenAnswer(StudentAnswer)
asm_crud = CRUDAssignment(Assignment)

question_crud = CRUDQuestion(Question)
llm = AzureOpenAI(
    azure_endpoint=settings.AZURE_ENDPOINT,
    api_key=settings.AZURE_API_KEY,
    api_version=settings.AZURE_API_VERSION,
)

initial_prompt = "I want you to act as an AI evaluating students' coding work. I will provide you a text file of the coding question with points of the question in brackets (example: Question 1 (8pts)) and a text file of the standard marking criteria that you will need to follow to give recommended marks. I will provide you with a folder containing coding works in text format and your task is to use artificial intelligence tools, such as natural language processing, to detect the programming language, give tailored feedback on how they can improve and write it in the Feedback section, only give 1 total recommended mark of the question point in the Score section, separated by a break line. Only use the marking criteria for standardizing the mark, do not give a mark completely based on the provided marking criteria. Here are the marking criteria, test questions, and the students' work in text: "

async def divide_into_each_question(result):
    pass

async def bulk_create_result(ids, result, db):
    print(ids)
    print(result)
    

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
        for sa in sas:
            if current_student_name and sa.student_name != current_student_name: 
                prompt = " ".join(
                    [initial_prompt, marking_criteria, question_content, processed]
                )
                messages = [
                    {
                        "role": "system",
                        # "content": "You are a teacher assistant who help to grade student code assesment.",
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
                bulk_create_result(accumulate_ids, completion.choices[0].message.content, db)
                accumulate_ids = []
                processed = ""
                    
            current_student_name = sa.student_name
            accumulate_ids.append(sa.id)
            processed += sa.protected_answer + "\n"

        # with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        #     for file_name in zip_ref.namelist():
        #         with zip_ref.open(file_name) as extracted_file:
        #             student_name, question_number = common.extract_student_info(file_name)
        #             q = question_crud.read_by_title(student_answer_data.assignment_id, question_number, db)
        #             if not q:
        #                 print("found no question")
        #                 continue
        #             file_data = extracted_file.read()
        #             student_answer = file_data.decode('utf-8')
        #             prompt = " ".join(
        #                 [initial_prompt, q.instruction, student_answer, q.marking_criteria]
        #             )
        #             messages = [
        #                 {
        #                     "role": "system",
        #                     "content": "You are a teacher assistant who help to grade student code assesment.",
        #                 },
        #                 {"role": "user", "content": prompt},
        #             ]
        #             completion = llm.chat.completions.create(
        #                 model="AzureCodeGrader",
        #                 messages=messages,
        #                 temperature=0.7,
        #                 max_tokens=800,
        #                 top_p=0.95,
        #                 frequency_penalty=0,
        #                 presence_penalty=0,
        #                 stop=None,
        #             )
        #             sa_dict = student_answer_data.__dict__
        #             sa_dict["result"] = completion.choices[0].message.content
        #             sa_dict["answer"] = student_answer
        #             sa_dict["student_name"] = student_name
        #             sa_dict["question_id"] = q.id
        #             sa_dict["question_title"] = q.question_title
        #             await sa_crud.create(sa_dict, db)
