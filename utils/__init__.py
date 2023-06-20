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