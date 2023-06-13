from .application import app
from flask import render_template, Response, send_from_directory, make_response
from http import HTTPStatus
from flask import request
import os
import openai
from utils.chains import *
from utils.openai_utils import *
from utils.file_manager import *

# create a route for webhook that accepts POST requests
@app.route("/webhook", methods=["POST"])
def webhook():
    # return response
    return make_response("This is a webhook response", HTTPStatus.OK)

# create a ping route
@app.route("/ping", methods=["GET"])
def ping():
    # return response
    return make_response("This is a ping response", HTTPStatus.OK)

# create a route to prompt gpt-3 to generate a response 
# the key is stored in env.OPENAI_API_KEY
@app.route("/generate", methods=["POST"])
def generate():
    # get prompt from request body
    prompt = request.json["prompt"]
    gpt_response =  post_to_gpt(prompt)
    # call extra processors if needed
    return gpt_response

# create a route to obtain pdfs and a prompt
@app.route("/generate_response_from_pdf", methods=["POST"])
def generate_response_from_pdf():
    # get prompt from request body
    pdf_url = request.json["pdf_path"]
    # download pdf from url
    pdf_path = download_pdf(pdf_url)
    prompt = request.json["prompt"]
    generator = ContextBasedGenerator(pdf_path)
    gpt_response = generator.generate_chain_response(prompt)
    # call extra processors if needed
    return gpt_response