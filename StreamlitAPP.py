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