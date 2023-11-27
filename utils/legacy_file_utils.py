import requests
import re
from . import *
from datetime import datetime
import json
import time
from .file_utils import *

client_id="<TOFILL>"
token="<TOFILL>"



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
    polling_response_json = poll_html_to_pdf_conversion(3, poll_uri)
    
    return polling_response_json