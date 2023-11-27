import requests
import re
from . import *
from datetime import datetime
import json
import time
from utils.openai_utils import post_to_dalle_parallel

def download_pdf(url, chunk_size = 2000):
    r = requests.get(url, stream=True)
    file_name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    pdf_path = os.path.join(pdfs_dir, file_name+".pdf")
    with open(pdf_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    return pdf_path 

def replace_form_action(html_data, new_action):
    updated_html = html_data.replace('\n', '')
    index = updated_html.find('<')
    if index != -1:
        updated_html = updated_html[index:]
    pattern = r'<form\s+[^>]*\baction\s*=\s*["\']([^"\']*)["\']'
    repl = '<form action="{}"'.format(new_action)
    updated_html = re.sub(pattern, repl, updated_html, count=1)
    # print(updated_html)
    return updated_html

def html2pdf(html_string):
    url = "https://yakpdf.p.rapidapi.com/pdf"

    payload = {
    "source": { "html": f"{html_string}" },
    "pdf": {
        "format": "A4",
        "scale": 1,
        "printBackground": True,
        "margin": {
            "top": "1in",
            "bottom": "1in",
            "left": "0.5in",
            "right": "0.5in"
        }
    },
    "wait": {
        "for": "navigation",
        "waitUntil": "load",
        "timeout": 2500
    }
    }
    headers = {
    "content-type": "application/json",
    "x-api-key": "none",
    "X-RapidAPI-Key": "<TOFILL>",
    "X-RapidAPI-Host": "yakpdf.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    file_name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".pdf"
    file_path = os.path.join(responses_dir, file_name)
    with open(file_path, "wb") as f:
        f.write(response.content)
    return file_name

def process_html(html_string):
    html_processed = replace_form_action(html_string, 'mailto:<TOFILL>')
    html_processed = replace_image_in_html(html_processed)
    return html_processed

def write_html(html_string, dir=""):
   file_name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".html"
   file_path = os.path.join(responses_dir, file_name)
   with open(file_path, "w") as f:
        f.write(html_string)
   print("HTML written to file: ", file_name)
   return file_path

def find_alt_in_image_tag(img_tag):
    # find alt tag using regex inside image tags <img >
    pattern = r'alt\s*=\s*["\']([^"\']*)["\']'
    alt_text = re.search(pattern, img_tag)
    if alt_text is None:
        return ""
    return alt_text.group(1)

def replace_image_in_html(html_string):
    # find all image start(<) to end(>) indices using regex
    pattern = r'<img\s+[^>]*>'
    img_starts = [m.start() for m in re.finditer(pattern, html_string)]
    img_ends = [m.end() for m in re.finditer(pattern, html_string)]
    img_tags = [html_string[img_start:img_end] for img_start, img_end in zip(img_starts, img_ends)]

    # find alt text for each image tag
    alt_texts = []
    for img_tag in img_tags:
        alt_text = find_alt_in_image_tag(img_tag)
        if(alt_text == ""):
            print("!!!Removing image: alt not found")
            img_tags.remove(img_tag)
            continue
        alt_texts.append(alt_text)

    # send each element of alt_texts parallelly to dalle and store responses in post_responses
    post_responses = post_to_dalle_parallel(alt_texts)
    new_img_tags = []
    for img_tag, dalle_response in zip(img_tags, post_responses):
        # replace src with dalle response
        #find src tag using regex inside image tags <img >
        pattern = r'src\s*=\s*["\']([^"\']*)["\']'
        src_text = re.search(pattern, img_tag)
        src_start = src_text.start(1)
        src_end = src_text.end(1)
        if src_start == -1 or src_end == -1:
           img_tags.remove(img_tag)
           print("!!!Removing image: src not found")
           continue
        new_image_tag = img_tag[:src_start] + dalle_response + img_tag[src_end:]
        new_img_tags.append(new_image_tag)

    for old_img_tag, new_img_tag in zip(img_tags, new_img_tags):
        # replace old image tag with new image tag
        new_img_tag = f'<center>{new_img_tag}</center>'
        html_string = html_string.replace(old_img_tag, new_img_tag)
    return html_string