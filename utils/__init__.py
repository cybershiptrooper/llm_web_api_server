import openai
import os

# import requests
# import pathlib
# import subprocess
# import tempfile

openai.api_key = "----"
os.environ["OPENAI_API_KEY"] = "----"
# os.environ["OPENAI_API_KEY"] = "----"
# os.environ["OPENAI_API_VERSION"]="2023-03-15-preview"

# file directories
db_dir = os.path.join(os.path.dirname(__file__), "../storage/db")
pdfs_dir = os.path.join(os.path.dirname(__file__), "../storage/pdfs")
responses_dir = os.path.join(os.path.dirname(__file__), "../storage/test_responses")