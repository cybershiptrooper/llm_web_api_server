import requests
import re
from . import *
from datetime import datetime
import json
import time

client_id="38c17d66d1ef4e9b96f5d094cdd1b6e3"
token="eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEta2V5LWF0LTEuY2VyIiwia2lkIjoiaW1zX25hMS1rZXktYXQtMSIsIml0dCI6ImF0In0.eyJpZCI6IjE2ODY3MjcxMTk1NzZfMWIxY2E2MzEtMTEyZi00YjVjLWFiNjgtMGNmNjY2YThiOWQ5X3V3MiIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiIzOGMxN2Q2NmQxZWY0ZTliOTZmNWQwOTRjZGQxYjZlMyIsInVzZXJfaWQiOiJGNUIxMUVERjY0ODk2OTQwMEE0OTVFMzRAdGVjaGFjY3QuYWRvYmUuY29tIiwiYXMiOiJpbXMtbmExIiwiYWFfaWQiOiJGNUIxMUVERjY0ODk2OTQwMEE0OTVFMzRAdGVjaGFjY3QuYWRvYmUuY29tIiwiY3RwIjozLCJmZyI6IlhRWjVNWUk0RlBQNU1QNEtFTVFWWkhBQUpVPT09PT09IiwibW9pIjoiZmU4MDEyNTUiLCJleHBpcmVzX2luIjoiODY0MDAwMDAiLCJzY29wZSI6Im9wZW5pZCxEQ0FQSSxBZG9iZUlELGFkZGl0aW9uYWxfaW5mby5vcHRpb25hbEFncmVlbWVudHMiLCJjcmVhdGVkX2F0IjoiMTY4NjcyNzExOTU3NiJ9.ANIBP2SAPZ7vhm8weGkpQGvQ2FaHv4An2C0bhVjB9_tKHB3hSzIo9PyeBPuMyRkqfYBFEYP8DF-IFnbLQRyAmZIcagjgX0nHniSDSOrgEHdnUHuFK380zIQKvYMwCTjLEKTJpfV1oOMaaUow6gKz7yjFLfgalqsAx9gcaa8QLeO0tCS6kdFx4Rx_TNqJfdKZlRK8r1NCLk5j0YldEMo74ftywfm6V73EvEf8fpRvXDGKnojq7qhcMs3ZeTg7frG_KBeg5f61B79C6FwJGBqyJfo0tKeN5VUM803K5vQ8V7A6l8uSAcBACulWcnHnpoXVs3KZ2I4w8T07Lk9Xcq0UAA"

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

# def html2pdfNew(html_string):
#   url = "https://yakpdf.p.rapidapi.com/pdf"

#   payload = {
#     "source": { "html": f"{html_string}" },
#     "pdf": {
#       "format": "A4",
#       "scale": 1,
#       "printBackground": True
#     },
#     "wait": {
#       "for": "navigation",
#       "waitUntil": "load",
#       "timeout": 2500
#     }
#   }
#   headers = {
#     "content-type": "application/json",
#     "x-api-key": "none",
#     "X-RapidAPI-Key": "b4cd2bfc17msh566656031a54132p121277jsn1bb63ca95415",
#     "X-RapidAPI-Host": "yakpdf.p.rapidapi.com"
#   }

#   response = requests.post(url, json=payload, headers=headers)
#   return response.content
