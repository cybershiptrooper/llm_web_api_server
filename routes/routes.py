from .application import app
from flask import render_template, Response, send_from_directory, make_response
from http import HTTPStatus
from flask import request
import os
import openai

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
    gpt_request = {
        "engine": "text-davinci-003",
        "temperature": 0.2,
        "max_tokens": 2000,
        "top_p": 1,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "prompt": prompt,
    }
    print("===========", os.getenv("OPENAPI"), "===========")
    openai.api_key = os.getenv("OPENAPI")
    response = openai.Completion.create(**gpt_request)
    return response


    