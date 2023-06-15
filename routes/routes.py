from .routes_impl import *
from .debug_routes import *
from .pdf_routes import *

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

@app.route("/generate_html_from_pdf", methods=["POST"])
def generate_html_response():
    # get prompt from request body
    prompt = request.form["prompt"]
    
    # get pdf from path
    num_files = int(request.form["num_files"])
    if num_files == 0:
        return make_response("No pdfs given", HTTPStatus.INTERNAL_SERVER_ERROR)
    pdf_paths = []
    for i in range(1, num_files+1):
        try:
            file = request.files[f'file{i}']
            pdf_paths.append(get_pdf_from_client(file))
        except Exception as e:
            try:
                file = request.form[f'file{i}']
                pdf_paths.append(download_pdf(file))
            except Exception as e:
                print(e)
                return make_response("Error getting pdf", HTTPStatus.INTERNAL_SERVER_ERROR)

    # generate response
    try:
        print(pdf_paths)
        return make_response(get_gpt_response(prompt, pdf_paths), HTTPStatus.OK)
    except Exception as e:
        print(e)
        return make_response("Error generating response", HTTPStatus.INTERNAL_SERVER_ERROR)

