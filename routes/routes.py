from .routes_impl import *
from .debug_routes import *
from .pdf_routes import *
import json

html_sample=".\n\n<!DOCTYPE html>\n<html>\n<head>\n<style>\nh1 {\n    font-family: sans-serif;\n    font-size: 1.5em;\n    text-align: center;\n    color: #3A3A3A;\n}\n\nform {\n    font-family: sans-serif;\n    font-size: 1em;\n    color: #3A3A3A;\n    padding: 10px;\n    border: 1px solid #3A3A3A;\n    border-radius: 5px;\n    margin: 0 auto;\n    width: 400px;\n}\n\ninput[type=text], select {\n    width: 100%;\n    padding: 12px 20px;\n    margin: 8px 0;\n    display: inline-block;\n    border: 1px solid #ccc;\n    border-radius: 4px;\n    box-sizing: border-box;\n}\n\ninput[type=submit] {\n    width: 100%;\n    background-color: #3A3A3A;\n    color: white;\n    padding: 14px 20px;\n    margin: 8px 0;\n    border: none;\n    border-radius: 4px;\n    cursor: pointer;\n}\n\ninput[type=submit]:hover {\n    background-color: #454545;\n}\n\ndiv {\n    border-radius: 5px;\n    background-color: #f2f2f2;\n    padding: 20px;\n}\n</style>\n</head>\n<body>\n\n<h1>BeneFit Customer Acquisition Form</h1>\n\n<div>\n  <form action=\"/action_page.php\">\n    <label for=\"name\">Name</label>\n    <input type=\"text\" id=\"name\" name=\"name\" placeholder=\"Your name..\">\n\n    <label for=\"email\">Email</label>\n    <input type=\"text\" id=\"email\" name=\"email\" placeholder=\"Your email..\">\n\n    <label for=\"phone\">Phone Number</label>\n    <input type=\"text\" id=\"phone\" name=\"phone\" placeholder=\"Your phone number..\">\n\n    <label for=\"membership\">Membership Type</label>\n    <select id=\"membership\" name=\"membership\">\n      <option value=\"basic\">Basic</option>\n      <option value=\"premium\">Premium</option>\n    </select>\n\n    <input type=\"submit\" value=\"Submit\">\n  </form>\n</div>\n\n</body>\n</html>"
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

# # create a route to obtain pdfs and a prompt
# @app.route("/generate_html_from_pdf", methods=["POST"])
# def generate_html_response_from_pdf():
#     # get prompt from request body
#     prompt = request.form["prompt"]
    
#     # get pdf from path
#     file = request.files['file']
#     # pdf_path = download_pdf(pdf_url)
#     pdf_path = get_pdf_from_client(file)
    
#     # generate response
#     try:
#         return make_response(get_gpt_response(prompt, pdf_path), HTTPStatus.OK)
#     except Exception as e:
#         print(e)
#         return make_response("Error generating response", HTTPStatus.INTERNAL_SERVER_ERROR)

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

@app.route("/get_url", methods=["GET"])
def get_url():
    # generate response
    try:
        response = get_upload_url()
        print(response)
    except Exception as e:
        print(e)
        return make_response("Error generating response", HTTPStatus.INTERNAL_SERVER_ERROR)
    return make_response(response.content, HTTPStatus.OK)

@app.route("/get_document_from_html", methods=["GET"])
def get_document_from_html():
    # generate response
    try:
        upload_url_response = get_upload_url()
        upload_url_response_json = json.loads(upload_url_response.content)
        # print(upload_url_response.content)
        # print(upload_url_response_json)
        # Extract the value from the JSON response
        #value = json_response.get('value')
        # Return the extracted value
        html_string = replace_form_action(html_sample, 'mailto:nikhilarora@adobe.com')
        asset_id = upload_url_response_json.get('assetID')
        uploadUri = upload_url_response_json.get('uploadUri')
        # print(uploadUri)
        upload_html_response = upload_html(uploadUri, html_string)
        print(upload_html_response.content)
        # print("Printing asset ID next")
        # print(asset_id)
        download_url_response = get_download_url(asset_id)
        download_url_response_json = json.loads(download_url_response.content)
        downloadUri = download_url_response_json.get('downloadUri')
        print("Printing downloadUri next")
        print(downloadUri)
        html_to_pdf_response = schedule_html_to_pdf_conversion(downloadUri)
        html_to_pdf_response_headers = dict(html_to_pdf_response.headers)
        print("html to pdf api response")
        print(html_to_pdf_response.content)
        print("Printing headers next")
        print(html_to_pdf_response_headers)
        poll_uri = html_to_pdf_response_headers.get('location')    
        polling_response_json = poll_html_to_pdf_conversion(3, poll_uri)

    except Exception as e:
        print(e)
        return make_response("Error generating response", HTTPStatus.INTERNAL_SERVER_ERROR)
    return make_response(polling_response_json, HTTPStatus.OK)
