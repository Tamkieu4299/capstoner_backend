from flair.data import Sentence
from flair.models import SequenceTagger
from app.constants.config import Settings
from app.models.student_answer_model import StudentAnswer
from app.crud.student_answer_crud import CRUDStudenAnswer
from app.models.removed_word_model import RemovedWords
from app.crud.removed_word_crud import CRUDRemovedWord
import flair
import re

settings = Settings()
print(flair.cache_root)
# Load the Flair NER model
tagger = SequenceTagger.load("ner")
sa_crud = CRUDStudenAnswer(StudentAnswer)
rw_crud = CRUDRemovedWord(RemovedWords)

# Function to detect sensitive information using regex and Flair NER
def detect_sensitive_info(text):
    sensitive_info = []
    
    # Regex pattern for email addresses and long alphanumeric strings (e.g., student IDs)
    generic_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b|\b[A-Za-z0-9]{8,}\b')
    
    # Create a sentence object for Flair
    sentence = Sentence(text)
    
    # Use Flair to tag the sentence
    tagger.predict(sentence)
    
    # Extract entities
    entities = [entity.text for entity in sentence.get_spans('ner') if entity.tag in ["PER", "ORG", "LOC"]]
    
    # Combine regex matches and Flair NER entities
    matches = generic_pattern.findall(text) + entities

    # Sort matches by their position in the text to maintain order
    matches = sorted(set(matches), key=lambda x: text.find(x))

    for match in matches:
        if not any(match in info for info in sensitive_info):
            sensitive_info.append(match)

    return sensitive_info

def privacy_protection_processor(assignment_id):
    sessionmaker = settings.psql_factory.create_sessionmaker()
    with sessionmaker() as db:
        sas = sa_crud.read_by_assignment_id(assignment_id, db)
        print(sas)
        for sa in sas:
            bulk_data = []
            sensi_data = detect_sensitive_info(sa.answer)
            print("sensiiiiii")
            print(sensi_data)
            for idx, sd in enumerate(sensi_data):
                bulk_data.append({
                    "student_answer_id": sa.id,
                    "original_value": sd,
                    "order": idx
                })
            print("bulkkkk")
            print(bulk_data)
            rw_crud.bulk_create(bulk_data, db)

    # pass