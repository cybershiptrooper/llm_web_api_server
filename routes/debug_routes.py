from .routes_impl import *

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