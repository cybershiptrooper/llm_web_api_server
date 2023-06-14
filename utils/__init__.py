import openai
import os

# import requests
# import pathlib
# import subprocess
# import tempfile

openai.api_key = "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"
os.environ["OPENAI_API_KEY"] = "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"

# file directories
db_dir = os.path.join(os.path.dirname(__file__), "../storage/db")
pdfs_dir = os.path.join(os.path.dirname(__file__), "../storage/pdfs")
responses_dir = os.path.join(os.path.dirname(__file__), "../storage/test_responses")