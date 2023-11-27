from .routes_impl import *
import json 

# create a ping route
@app.route("/ping", methods=["GET"])
def ping():
    # return response
    return make_response("This is a ping response", HTTPStatus.OK)

@app.route("/get_pdf", methods=["POST"])
def get_pdf():
    # get prompt from request body
    pdf_url = request.json["pdf_url"]
    # download pdf from url
    try:
        pdf_path = download_pdf(pdf_url)
    except Exception as e:
        print(e)
        return make_response("Error downloading pdf", HTTPStatus.INTERNAL_SERVER_ERROR)
    return make_response("success", HTTPStatus.OK)

@app.route('/upload', methods = ['POST'])
def upload_file():
    f = request.files['file']
    try:
        path = get_pdf_from_client(f)
        return make_response(path, HTTPStatus.OK)
    except Exception as e:
        print(e)
        return make_response("Error uploading pdf", HTTPStatus.INTERNAL_SERVER_ERROR)

@app.route("/get_html_no_prompt_check", methods=["POST"])
def get_html_no_prompt_check():
    # get prompt from request body
    file_dir = os.path.dirname(__file__)
    reponses_dir = os.path.join(file_dir, "../storage/test_responses")
    prompt = request.json["prompt"]
    with open(os.path.join(reponses_dir, "vvold.html") , "r") as f:
        doc = f.read()
    return make_response(doc, HTTPStatus.OK)

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

@app.route("/get_document_from_html_sample", methods=["GET"])
def get_document_from_html_sample():
    html_sample=".\n\n<!DOCTYPE html>\n<html>\n<head>\n<style>\nh1 {\n    font-family: sans-serif;\n    font-size: 1.5em;\n    text-align: center;\n    color: #3A3A3A;\n}\n\nform {\n    font-family: sans-serif;\n    font-size: 1em;\n    color: #3A3A3A;\n    padding: 10px;\n    border: 1px solid #3A3A3A;\n    border-radius: 5px;\n    margin: 0 auto;\n    width: 400px;\n}\n\ninput[type=text], select {\n    width: 100%;\n    padding: 12px 20px;\n    margin: 8px 0;\n    display: inline-block;\n    border: 1px solid #ccc;\n    border-radius: 4px;\n    box-sizing: border-box;\n}\n\ninput[type=submit] {\n    width: 100%;\n    background-color: #3A3A3A;\n    color: white;\n    padding: 14px 20px;\n    margin: 8px 0;\n    border: none;\n    border-radius: 4px;\n    cursor: pointer;\n}\n\ninput[type=submit]:hover {\n    background-color: #454545;\n}\n\ndiv {\n    border-radius: 5px;\n    background-color: #f2f2f2;\n    padding: 20px;\n}\n</style>\n</head>\n<body>\n\n<h1>BeneFit Customer Acquisition Form</h1>\n\n<div>\n  <form action=\"/action_page.php\">\n    <label for=\"name\">Name</label>\n    <input type=\"text\" id=\"name\" name=\"name\" placeholder=\"Your name..\">\n\n    <label for=\"email\">Email</label>\n    <input type=\"text\" id=\"email\" name=\"email\" placeholder=\"Your email..\">\n\n    <label for=\"phone\">Phone Number</label>\n    <input type=\"text\" id=\"phone\" name=\"phone\" placeholder=\"Your phone number..\">\n\n    <label for=\"membership\">Membership Type</label>\n    <select id=\"membership\" name=\"membership\">\n      <option value=\"basic\">Basic</option>\n      <option value=\"premium\">Premium</option>\n    </select>\n\n    <input type=\"submit\" value=\"Submit\">\n  </form>\n</div>\n\n</body>\n</html>"
    # generate response
    try:
        upload_url_response = get_upload_url()
        upload_url_response_json = json.loads(upload_url_response.content)
        # print(upload_url_response.content)
        # print(upload_url_response_json)
        # Extract the value from the JSON response
        #value = json_response.get('value')
        # Return the extracted value
        html_string = replace_form_action(html_sample, 'mailto:<TOFILL>')
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
        polling_response_json = poll_html_to_pdf_conversion(1.5, poll_uri)

    except Exception as e:
        print(e)
        return make_response("Error generating response", HTTPStatus.INTERNAL_SERVER_ERROR)
    return make_response(polling_response_json, HTTPStatus.OK)

@app.route("/get_document_from_pdf_sample", methods=["GET", "POST"])
def get_document_from_pdf_sample():
    file = "storage/test_pdfs/test_image.html_str"
    with open(file, "r") as f:
        html_string = f.read()
    html_processed = process_html(html_string)
    pdf_old = html2pdf(html_processed)
    dict = {
        "asset": {
            "downloadUri" : f"{server}/pdfs/{pdf_old}",
        }
    }
    return make_response(dict, HTTPStatus.OK)


@app.route("/get_response_from_firefall", methods=["POST"])
def get_response_from_firefall():
    prompt_json = request.json
    user_prompt = prompt_json.get('dialogue')
    response = post_to_gpt_firefall(user_prompt)
    response_json = response.json()
    print(response.json)
    html = response_json["generations"][0][0]["text"]
    return make_response(html, HTTPStatus.OK)


@app.route("/get_response_from_azure", methods=["POST"])
def get_response_from_azure():
    prompt_json = request.json
    user_prompt = prompt_json.get('dialogue')
    response = post_to_gpt_azure(user_prompt)
    response_json = response.json()
    print(response.json)
    html = response_json["choices"][0]["message"]
    return make_response(html, HTTPStatus.OK)
    