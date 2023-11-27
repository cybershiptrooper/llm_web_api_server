from utils.file_utils import *
import os
def test_replace_form_action():
    html_string = '<form action="https://www.w3docs.com/action_page.php">'
    expected_html_string = '<form action="mailto:<TOFILL>">'
    assert replace_form_action(html_string, 'mailto:<TOFILL>') == expected_html_string

def test_replace_form_action_on_file():
    file = "storage/test_pdfs/15_06_2023_11_48_26.html_str"
    with open(file, "r") as f:
        html_string = f.read()
    html_processed = replace_form_action(html_string, 'mailto:<TOFILL>')
    out_file = "storage/test_responses/test_replace_form_action_on_file_out.html"
    with open(out_file, "w") as f:
        f.write(html_processed)

def test_replace_image_in_html():
    file = "storage/test_pdfs/test_image.html_str"
    with open(file, "r") as f:
        html_string = f.read()
    html_processed = replace_image_in_html(html_string)
    out_file = "storage/test_responses/test_replace_image_in_html_out.html"
    with open(out_file, "w") as f:
        f.write(html_processed)

def test_html2pdf():
    file = "storage/test_pdfs/test_image.html_str"
    with open(file, "r") as f:
        html_string = f.read()
    html_processed = process_html(html_string)
    pdf = html2pdf(html_processed)
    print(pdf)
