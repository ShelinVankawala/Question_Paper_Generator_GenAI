import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging


from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

# loading the enviorment variables
load_dotenv()
# get the key
KEY = os.getenv("OPEN_AI_KEY")


# create the openai llm client
llm = ChatOpenAI(openai_api_key = KEY, model_name="gpt-3.5-turbo",
                 temperature=0.3)

# This is the template i will pass
TEMPLATE="""
Text: {text}
You are an expert in creating MCQs and detailed answer questions. Given the above text, your task is to create a quiz comprising {mcq_number} multiple choice questions (MCQs), {three_marks_number} questions worth 3 marks, and {five_marks_number} questions worth 5 marks for {subject} students. Maintain a {tone} tone throughout the quiz. 
Ensure the questions are unique, relevant to the provided text, and that they accurately assess the students' understanding of the subject matter.
Adhere to the following format in your RESPONSE_JSON below as a guide. Create {mcq_number} MCQs, {three_marks_number} questions for 3 marks, and {five_marks_number} questions for 5 marks, ensuring a comprehensive evaluation.

{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "mcq_number", "three_marks_number", "five_marks_number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

TEMPLATE2 = """
You are an expert English grammarian and writer. Given a comprehensive quiz for {subject} students, including multiple choice questions (MCQs), questions worth 3 marks, and questions worth 5 marks, your task is to evaluate the overall complexity of the quiz. Provide a succinct complexity analysis, not exceeding 50 words. Assess whether the quiz aligns with the cognitive and analytical abilities of the intended student audience. 

If you find any aspects of the quiz not up to par—whether it be the content, cognitive demands, or tone—identify these issues specifically. Suggest necessary modifications to ensure the quiz questions are appropriately challenging and engaging, and adjust the tone to perfectly match the students' abilities.

Content:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2,
)

review_chain = LLMChain(llm=llm,
                        prompt=quiz_evaluation_prompt,
                        output_key="review",
                        verbose=True)

generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "mcq_number", "three_marks_number", "five_marks_number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True
)