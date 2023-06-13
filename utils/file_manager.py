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