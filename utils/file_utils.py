import requests
import re
from . import *
from datetime import datetime

def download_pdf(url, chunk_size = 2000):
  r = requests.get(url, stream=True)
  file_name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
  pdf_path = os.path.join(pdfs_dir, file_name)
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
  print(updated_html)
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