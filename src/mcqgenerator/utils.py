import os
import json
import PyPDF2
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file) 
            text=""
            for page in pdf_reader.pages:
                text+ page.extract_text()
            return text
        except Exception as e:
            raise Exception("error reading the PDF file")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
            raise Exception(
            "unsupported file format only pdf and text file suppoted"
            )
def get_table_data(quiz_str):
    try:
# convert the quiz from a str to dict
        quiz_data=json.loads(quiz_str)
        quiz_table_data=[]
        for key, value in quiz_data.items():
            if "mcq" in value:
                mcq = value["mcq"]
                options = " | ".join([f"{option}: {option_value}" for option, option_value in value["options"].items()])
                correct = value["correct"]
                quiz_table_data.append({"Question Type": "MCQ", "Question": mcq, "Options": options, "Correct Answer": correct})

        # Process three marks questions
        for key, value in quiz_data.items():
            if "three_marks_questions" in value:
                question = value["three_marks_questions"]
                quiz_table_data.append({"Question Type": "Three Marks", "Question": question})

        # Process five marks questions
        for key, value in quiz_data.items():
            if "five_marks_questions" in value:
                question = value["five_marks_questions"]
                quiz_table_data.append({"Question Type": "Five Marks", "Question": question})
                
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False