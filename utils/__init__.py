import openai
import os

# import requests
# import pathlib
# import subprocess
# import tempfile

openai.api_key = os.getenv("OPENAPI")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAPI")

# file directories
db_dir = os.path.join(os.path.dirname(__file__), "../storage/db")
pdfs_dir = os.path.join(os.path.dirname(__file__), "../storage/pdfs")