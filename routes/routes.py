from .application import app
from flask import render_template, Response, send_from_directory, make_response
from http import HTTPStatus
from flask import request
import os
import openai
from utils.chains import *
from utils.openai_utils import *
from utils.file_utils import *

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

@app.route("/generate_html_from_prompt", methods=["POST"])
def generate_html_response_from_prompt():
    # get prompt from request body
    prompt = request.json["prompt"]
    prompt = f"You are a document creator that creates html files based on prompts. The output should be a valid html. You may include css in the html script. Now create a document for the user prompt: {prompt} \n"
    gpt_response =  post_to_gpt(prompt)
    # call extra processors if needed
    return gpt_response

# create a route to obtain pdfs and a prompt
@app.route("/generate_html_from_pdf", methods=["POST"])
def generate_html_response_from_pdf():
    # get prompt from request body
    pdf_url = request.json["pdf_url"]
    # download pdf from url
    pdf_path = download_pdf(pdf_url)
    prompt = request.json["prompt"]
    generator = ContextBasedGenerator(pdf_path)
    print("Initialized generator")
    try:
        gpt_response = generator.generate_chain_response(prompt)
        print("obtained response:")
        print(gpt_response)
        # call extra processors if needed
        return make_response(gpt_response[0]["text"], HTTPStatus.OK)
    except Exception as e:
        print(e)
        return make_response("Error generating response", HTTPStatus.INTERNAL_SERVER_ERROR)
    

@app.route("/get_html_no_prompt_check", methods=["POST"])
def get_html_no_prompt_check():
    # get prompt from request body
    file_dir = os.path.dirname(__file__)
    reponses_dir = os.path.join(file_dir, "../storage/test_responses")
    prompt = request.json["prompt"]
    with open(os.path.join(reponses_dir, "vvold.html") , "r") as f:
        doc = f.read()
    return make_response(doc, HTTPStatus.OK)

@app.route("/cvt_html_to_pdf", methods=["POST"])
def cvt_html_to_pdf():
    html_string = request.json["html"]
    pdf = html2pdf(html_string)
    return make_response(pdf, HTTPStatus.OK)

@app.route("/get_pdf_from_pdf", methods=["POST"])
def get_pdf_from_pdf():
    # get prompt from request body
    pdf_url = request.json["pdf_url"]
    # download pdf from url
    pdf_path = download_pdf(pdf_url)
    prompt = request.json["prompt"]
    generator = ContextBasedGenerator(pdf_path)
    print("Initialized generator")
    try:
        gpt_response = generator.generate_chain_response(prompt)
        print("obtained response:")
        print(gpt_response)
    except Exception as e:
        print(e)
        return make_response("Error generating response", HTTPStatus.INTERNAL_SERVER_ERROR)
    
    html_string = gpt_response[0]["text"]
    pdf = html2pdf(html_string)
    return make_response(pdf, HTTPStatus.OK)

@app.route("/generate_pdf_from_prompt", methods=["POST"])
def generate_pdf_response_from_prompt():
    # get prompt from request body
    prompt = request.json["prompt"]
    prompt = f"You are a document creator that creates html files based on prompts. The output should be a valid html. You may include css in the html script. Now create a document for the user prompt: {prompt} \n"
    gpt_response =  post_to_gpt(prompt)
    # call extra processors if needed
    pdf = html2pdf(gpt_response.content)
    return make_response(pdf, HTTPStatus.OK)

@app.route("/get_pdf_no_check", methods=["POST"])
def get_pdf_no_type_check():
    # get prompt from request body
    file_dir = os.path.dirname(__file__)
    reponses_dir = os.path.join(file_dir, "../storage/test_responses")
    _ = request.json["prompt"]
    with open(os.path.join(reponses_dir, "vvold.html") , "r") as f:
        doc = f.read()
    pdf = html2pdf(doc)
    return make_response(pdf, HTTPStatus.OK)