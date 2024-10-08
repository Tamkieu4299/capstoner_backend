import os
import zipfile
from app.models.assignment_model import Assignment
from app.models.student_answer_model import StudentAnswer
from app.crud.assignment_crud import CRUDAssignment
from app.crud.student_answer_crud import CRUDStudenAnswer
from app.constants.config import Settings
from ..utils import s3_driver, common
from charset_normalizer import from_bytes
import pymupdf  # imports the pymupdf library
import fitz

settings = Settings()

sa_crud = CRUDStudenAnswer(StudentAnswer)
asm_crud = CRUDAssignment(Assignment)

def detect_and_decode(data, is_pdf = False):
    if is_pdf:
        print("hereeeeeee")
        return data, "pdf"
    result = from_bytes(data).best()
    encoding = result.encoding
    return data.decode(encoding), encoding

def crop_question(question_data):
    lines = question_data.split('\n')
    questions_dict = {}
    current_question = None
    current_content = []

    for line in lines:
        if line.startswith("Question "):
            if current_question is not None:
                questions_dict[current_question] = ''.join(current_content).strip()
            current_question = f"question_{len(questions_dict) + 1}"
            current_content = []
        else:
            current_content.append(line)

    if current_question is not None:
        questions_dict[current_question] = ''.join(current_content).strip()

    return questions_dict

def count_questions(question_data):
    lines = question_data.split('\n')
    question_count = 0

    for line in lines:
        if line.startswith("Question "):
            question_count += 1

    return question_count

def read_file_content(file_name, extracted_file):
    # Check the file extension
    if file_name.endswith('.txt'):
        return extracted_file.read() # Assuming text files are UTF-8 encoded
    elif file_name.endswith('.pdf'):
        # Use PyMuPDF to read the content from a PDF
        with fitz.open(stream=extracted_file.read()) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text
    else:
        print(f"Unsupported file type: {file_name}")
    
async def create_assignment_processor(assignment_data, student_file_upload, student_file_zip, question_file, criteria_file):
    sessionmaker = settings.psql_factory.create_sessionmaker()
    with sessionmaker() as db:
        assignment_data_dict = assignment_data.__dict__

        # Question
        url_question = s3_driver.upload(file = question_file, dest_dir = assignment_data.name, protocol="")
        question_data = s3_driver.get_file(url_question)
        assignment_data_dict["questions_filepath"] = url_question
        assignment_data_dict["number_of_questions"] = count_questions(question_data)

        # Marking criteria
        url_criteria = s3_driver.upload(file = criteria_file, dest_dir = assignment_data.name, protocol="")
        assignment_data_dict["marking_criteria_filepath"] = url_criteria

        # Student answer
        url_sa = s3_driver.upload(file = student_file_upload, dest_dir = assignment_data.name, protocol="")
        assignment_data_dict["student_answer_filepath"] = url_sa

        # Add assignment into DB
        asm = await asm_crud.create(assignment_data_dict, db)
        
        with zipfile.ZipFile(student_file_zip, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                # Skip files in the __MACOSX directory and skip the 'demo 2/' directory itself
                if file_name.startswith('__MACOSX/') or file_name == 'demo 2/':
                    continue
                with zip_ref.open(file_name) as extracted_file:
                    student_name, question_title = common.extract_student_info(file_name)
                    file_data = read_file_content(file_name, extracted_file)
                    if not file_data:
                        print(f"File {file_name} is empty, skipping.")
                        continue
                    try:
                        student_answer, encoding = detect_and_decode(file_data, bool("pdf" in file_name))
                        print(f"Detected encoding for {file_name}: {encoding}")
                        sa_dict = {
                            "student_name": student_name,
                            "answer": student_answer,
                            "assignment_id": asm.id,
                            "question_title": question_title,
                        }
                        # Add student answer into DB
                        await sa_crud.create(sa_dict, db)
                    except:
                        print(f"Fail detected encoding for {file_name}")
                    

