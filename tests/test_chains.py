from utils.chains import *
from datetime import datetime
from . import *

def test_generate_db_from_pdf():
    pdf_path = os.path.join(pdfs_dir, "CS_781_Project.pdf")
    generator = ContextBasedGenerator(pdf_path)
    reponse = generator.generate_chain_response("Make an mcq quiz form with 3 questions in it.")
    try:
        time_ext = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        with open(os.path.join(test_responses_dir, f"test_generate_db_from_pdf_{time_ext}.html"), "w") as f:
            f.write(reponse[0]['text'])
    except Exception as e:
        print(reponse)
        raise Exception(f"response could not be written to file: {e}")
    assert True