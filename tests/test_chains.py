from utils.chains import *
import os
test_responses_dir = os.path.join(os.path.dirname(__file__), "../storage/test_responses")
pdfs_dir = os.path.join(os.path.dirname(__file__), "../storage/test_pdfs")
def test_generate_db_from_pdf():
    pdf_path = os.path.join(pdfs_dir, "CS_781_Project.pdf")
    generator = ContextBasedGenerator(pdf_path)
    reponse = generator.generate_chain_response("Make an mcq quiz form with 3 questions in it.")
    try:
        with open(os.path.join(test_responses_dir, "test_generate_db_from_pdf.html"), "w") as f:
            f.write(reponse[0]['text'])
    except:
        print(reponse)
        raise Exception("response could not be written to file")
    assert True