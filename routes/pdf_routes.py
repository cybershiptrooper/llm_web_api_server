from .routes_impl import *

@app.route("/cvt_html_to_pdf", methods=["POST"])
def cvt_html_to_pdf():
    html_string = request.json["html"]
    pdf = html2pdf(html_string)
    return make_response(pdf, HTTPStatus.OK)

@app.route("/pdfs/<path:path>")
def serve_pdf(path):
    print(path)
    file_dir = os.path.dirname(__file__)
    pdfs_dir = os.path.join(file_dir, "../storage/test_responses")
    return send_from_directory(pdfs_dir, path)

@app.route("/generate_pdf_from_prompt", methods=["POST"])
def generate_pdf_response_from_prompt():
    # get prompt from request body
    prompt = request.json["prompt"]
    prompt = f'You are a document creator that creates html files based on prompts. The output should be a valid html. You may include css, and up to 2 images in the html script. The image "alt" tag will be used as description for an image generation model to generate an image: its "src" tag should be an empty string and description should be in English. Do not add images unless necessary. Now create a document for the user prompt: {prompt} \n'
    gpt_response =  post_to_gpt(prompt)
    # call extra processors if needed
    write_html(gpt_response["choices"][0]["text"])
    html_processed = process_html(gpt_response["choices"][0]["text"])
    write_html(html_processed)
    file_name = html2pdf(html_processed)
    dict = {
        "asset": {
            "downloadUri" : f"{server}/pdfs/{file_name}",
        }
    }
    return make_response(dict, HTTPStatus.OK)

@app.route("/generate_pdf_from_pdf", methods=["POST"])
def generate_pdf_response_from_multiple_pdf():
    try:
        # get prompt from request body
        prompt = request.form["prompt"]
        
        # get pdf from path
        num_files = int(request.form["num_files"])
    except Exception as e:
        print(e)
        return make_response("Error getting prompt or num_files", HTTPStatus.INTERNAL_SERVER_ERROR)
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
        gpt_response = get_gpt_response(prompt, pdf_paths)
    except Exception as e:
        # TODO: add support for multiple pdfs
        print(e)
        return make_response("Error generating response", HTTPStatus.INTERNAL_SERVER_ERROR)
    # call extra processors if needed
    write_html(gpt_response)
    html_processed = process_html(gpt_response)
    write_html(html_processed)
    file_name = html2pdf(html_processed)
    dict = {
        "asset": {
            "downloadUri" : f"{server}/pdfs/{file_name}",
        }
    }
    return make_response(dict, HTTPStatus.OK)