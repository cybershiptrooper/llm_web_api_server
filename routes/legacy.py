from .routes_impl import *


@app.route("/legacy_get_pdf_from_pdf", methods=["POST"])
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

# create a route to obtain pdfs and a prompt
@app.route("/legacy_generate_html_from_pdf", methods=["POST"])
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