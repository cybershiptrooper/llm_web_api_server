from .application import app
from flask import render_template, Response, send_from_directory, make_response
from http import HTTPStatus
from flask import request
import os
import openai
from utils.chains import *
from utils.openai_utils import *
from utils.file_utils import *

def get_pdf_from_client(file):
    if(file.filename.endswith(".pdf")):
        file_path = os.path.join("storage/pdfs",file.filename)
        file.save(file_path)
    else:
        raise Exception("File must be a pdf")
    return file_path

def get_gpt_response(prompt, pdf_path):
    generator = ContextBasedGenerator(pdf_path)
    print("Initialized generator")
    gpt_response = generator.generate_chain_response(prompt)
    print("obtained response from gpt")
    # call extra processors if needed
    return gpt_response[0]["text"]