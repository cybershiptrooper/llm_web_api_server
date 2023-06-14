from .routes_impl import *
from .debug_routes import *

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
    prompt = request.form["prompt"]
    
    # get pdf from path
    file = request.files['file']
    # pdf_path = download_pdf(pdf_url)
    pdf_path = get_pdf_from_client(file)
    
    # generate response
    try:
        return make_response(get_gpt_response(prompt, pdf_path), HTTPStatus.OK)
    except Exception as e:
        print(e)
        return make_response("Error generating response", HTTPStatus.INTERNAL_SERVER_ERROR)

@app.route("/cvt_html_to_pdf", methods=["POST"])
def cvt_html_to_pdf():
    html_string = request.json["html"]
    pdf = html2pdf(html_string)
    return make_response(pdf, HTTPStatus.OK)

@app.route("/get_pdf_from_pdf", methods=["POST"])
def get_pdf_from_pdf():
    # get prompt from request body
    prompt = request.form["prompt"]
    
    # download pdf from url
    # pdf_url = request.json["pdf_url"]
    # pdf_path = download_pdf(pdf_url)
    file = request.files['file']
    pdf_path = get_pdf_from_client(file)
    
    # generate response
    try:
        gpt_response = get_gpt_response(prompt, pdf_path)
    except Exception as e:
        print(e)
        return make_response("Error generating response", HTTPStatus.INTERNAL_SERVER_ERROR)
    write_html(gpt_response)
    # call extra processors if needed
    pdf = html2pdf(gpt_response)
    return make_response(pdf, HTTPStatus.OK)

@app.route("/generate_pdf_from_prompt", methods=["POST"])
def generate_pdf_response_from_prompt():
    # get prompt from request body
    prompt = request.json["prompt"]
    prompt = f"You are a document creator that creates html files based on prompts. The output should be a valid html. You may include css in the html script. Now create a document for the user prompt: {prompt} \n"
    gpt_response =  post_to_gpt(prompt)
    # call extra processors if needed
    write_html(gpt_response["choices"][0]["text"])
    pdf = html2pdf(gpt_response["choices"][0]["text"])
    return make_response(pdf, HTTPStatus.OK)