from pypdf import PdfReader

def read_resume(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text     