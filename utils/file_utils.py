import requests
import re
from . import *
from datetime import datetime
import json
import time

client_id="b25781a590c344109846b56bfedd6aff"
token="eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEta2V5LWF0LTEuY2VyIiwia2lkIjoiaW1zX25hMS1rZXktYXQtMSIsIml0dCI6ImF0In0.eyJpZCI6IjE2ODY4MDg0MTA4NDNfMjI2NDgyZDQtNmYwNy00NjFjLTg5NjgtNzU0ZjkyZjFjMDdlX3VlMSIsIm9yZyI6IkY3RTkxRUUwNjQ4OTY1RUMwQTQ5NUNEOEBBZG9iZU9yZyIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiJiMjU3ODFhNTkwYzM0NDEwOTg0NmI1NmJmZWRkNmFmZiIsInVzZXJfaWQiOiJGMDZCMUVEQTY0ODk2NjMzMEE0OTVGQURAdGVjaGFjY3QuYWRvYmUuY29tIiwiYXMiOiJpbXMtbmExIiwiYWFfaWQiOiJGMDZCMUVEQTY0ODk2NjMzMEE0OTVGQURAdGVjaGFjY3QuYWRvYmUuY29tIiwiY3RwIjozLCJtb2kiOiJjMGNkYmM3NyIsImV4cGlyZXNfaW4iOiI4NjQwMDAwMCIsImNyZWF0ZWRfYXQiOiIxNjg2ODA4NDEwODQzIiwic2NvcGUiOiJvcGVuaWQsRENBUEksQWRvYmVJRCJ9.byBj7px5sWFxA42SRJMKzFwH-7c0SiHnhIGeAvvob9EYvZy9mDh2xnvXDJ9AMizCWPX9JGZOAs8ccqS7sU5_eMdLulJ8jKAPRy39zwJVToc2Wp2FYQTtEOcXQ8OAA8VKrqJD51f_2knQhPot6JETeW5-R0rvrH4FcCWlbVTmz1dcGNw9e9E2-VZfp1ff2PklOnvfBtuQmioLwX1ne_zn6P7DBuhLeDbci7g8GIZq-O9HwDjCIYnQb-d8MaeaLtpoE8jwxZC3Al-hkqhwcOJ5_QeJI2oktcfbdeA5FLATyohFM-S_DBE5P73J81gper-a6yiUnkYY0Q3HFmaJNzBg-g"

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
      "printBackground": True
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
    "X-RapidAPI-Key": "b4cd2bfc17msh566656031a54132p121277jsn1bb63ca95415",
    "X-RapidAPI-Host": "yakpdf.p.rapidapi.com"
  }

  response = requests.post(url, json=payload, headers=headers)
  return response.content

def write_html(html_string):
   file_name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".html"
   with open(os.path.join(responses_dir, file_name), "w") as f:
        f.write(html_string)

def get_upload_url():
  url = "https://pdf-services.adobe.io/assets"
  data = {
    "mediaType": "text/html"
  }
  headers = {
    "X-API-Key": client_id,
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
  }
  response = requests.post(url, json=data, headers=headers)
  return response

def upload_html(uploadUri, html_data):
  headers = {
    "Content-Type": "text/html",
  }
  response = requests.put(uploadUri, data=html_data, headers=headers)
  return response
  
def get_download_url(asset_id):
  url = "https://pdf-services.adobe.io/assets/" + asset_id
  headers = {
    "X-API-Key": client_id,
    "Authorization": "Bearer " + token,
  }
  response = requests.get(url, headers=headers)
  return response 

def schedule_html_to_pdf_conversion(download_url):
  url = "https://pdf-services-ue1.adobe.io/operation/htmltopdf"
  data = {
    "inputUrl": download_url,
    "json": "{}",
    "pageLayout": {
      "pageWidth": 11,
      "pageHeight": 8.5
    }
  }
  headers = {
    "X-API-Key": client_id,
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
  }
  response = requests.post(url, json=data, headers=headers)
  return response

def status_html_to_pdf_conversion(polling_url):
  headers = {
    "X-API-Key": client_id,
    "Authorization": "Bearer " + token,
  }
  response = requests.get(polling_url, headers=headers)
  return response 

def poll_html_to_pdf_conversion(polling_time_in_seconds, polling_url):
    while True:
        print("Polling...")
        status_response = status_html_to_pdf_conversion(polling_url)
        status_response_json = json.loads(status_response.content)
        status = status_response_json.get('status')
        if status != "in progress":
            return status_response_json
        time.sleep(polling_time_in_seconds)

def html2pdf_new(html_string):
    upload_url_response = get_upload_url()
    upload_url_response_json = json.loads(upload_url_response.content)
    # print(upload_url_response.content)
    # print(upload_url_response_json)
    # Extract the value from the JSON response
    #value = json_response.get('value')
    # Return the extracted value
    html_processed = replace_form_action(html_string, 'mailto:nikhilarora@adobe.com')
    asset_id = upload_url_response_json.get('assetID')
    uploadUri = upload_url_response_json.get('uploadUri')
    # print(uploadUri)
    upload_html_response = upload_html(uploadUri, html_processed)
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
    
    return polling_response_json
