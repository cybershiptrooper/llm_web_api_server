from utils.chains import *
from datetime import datetime
from . import *
from utils.chain_utils import *
import time

def test_generate_response_from_pdf():
    pdf_path = os.path.join(pdfs_dir, "CS_781_Project.pdf")
    start = time.time()
    generator = ContextBasedGenerator([pdf_path])
    end = time.time()
    print("Initialized generator: ", end-start)
    start = time.time()
    reponse = generator.generate_chain_response("Make an mcq quiz form with 3 questions in it.")
    end = time.time()
    print("obtained response from gpt: ", end-start)
    try:
        time_ext = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        with open(os.path.join(test_responses_dir, f"test_generate_db_from_pdf_{time_ext}.html"), "w") as f:
            f.write(reponse[0]['text'])
    except Exception as e:
        print(reponse)
        raise Exception(f"response could not be written to file: {e}")
    assert True

def test_generate_db_from_pdf():
    pdf_path = os.path.join(pdfs_dir, "CS_781_Project.pdf")
    start = time.time()
    generator = ContextBasedGenerator([pdf_path])
    end = time.time()
    print("Initialized generator: ", end-start)
    start = time.time()
    assert True

def test_get_generic_results():
    pdf_path = os.path.join(pdfs_dir, "CS_781_Project.pdf")
    start = time.time()
    generator = ContextBasedGenerator([pdf_path])
    end = time.time()
    print("Initialized generator: ", end-start)
    start = time.time()
    generator.get_generic_results()
    end = time.time()
    print("obtained response from gpt: ", end-start)
    assert True