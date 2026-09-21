from docx import Document
from datetime import datetime

def fill_contract(
    full_name: str,
    isikukood: str,
    specialty: str,
    gmail: str,
    phone_number: str,
    start_date: str,
    today_date: str,
    end_year: str,
    output_path: str
    ):
    doc = Document("KAPPI KASUTAMISE LEPING.docx")
    context = {
        "{FULL_NAME}": full_name,
        "{ISIKUKOOD}": isikukood,
        "{SPECIALTY}": specialty,
        "{GMAIL}": gmail,
        "{PHONE_NUMBER}": phone_number,
        "{START_DATE}": start_date,
        "{TODAY_DATE}": today_date,
        "{END_YEAR}": end_year
    }
    
    for words in doc.paragraphs:
        for key,value in context.items():
            if key in words.text:
                words.text = words.text.replace(key, str(value))
    
    doc.save(output_path)